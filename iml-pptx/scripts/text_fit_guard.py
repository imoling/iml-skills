#!/usr/bin/env python3
"""Heuristic PPTX text fit checker.

This script estimates whether editable text is likely too dense for its text
box. It is intentionally conservative and cannot replace screenshot QA.
"""

from __future__ import annotations

import argparse
import math
import re
import zipfile
from dataclasses import dataclass
from pathlib import Path
from xml.etree import ElementTree as ET


NS = {
    "p": "http://schemas.openxmlformats.org/presentationml/2006/main",
    "a": "http://schemas.openxmlformats.org/drawingml/2006/main",
}
EMU_PER_INCH = 914400


@dataclass
class TextBox:
    slide: str
    name: str
    x: float
    y: float
    w: float
    h: float
    text: str
    font_size: float


def emu_to_in(value: str | None) -> float:
    if not value:
        return 0.0
    return int(value) / EMU_PER_INCH


def font_size_pt(node: ET.Element) -> float:
    sizes: list[float] = []
    for rpr in node.findall(".//a:rPr", NS):
        sz = rpr.attrib.get("sz")
        if sz:
            sizes.append(int(sz) / 100)
    for defrpr in node.findall(".//a:defRPr", NS):
        sz = defrpr.attrib.get("sz")
        if sz:
            sizes.append(int(sz) / 100)
    return max(sizes) if sizes else 10.0


def read_text_boxes(pptx: Path) -> list[TextBox]:
    boxes: list[TextBox] = []
    with zipfile.ZipFile(pptx) as zf:
        slide_names = sorted(
            (n for n in zf.namelist() if re.match(r"ppt/slides/slide\d+\.xml$", n)),
            key=lambda n: int(re.search(r"slide(\d+)", n).group(1)),
        )
        for slide in slide_names:
            root = ET.fromstring(zf.read(slide))
            for node in root.findall(".//p:sp", NS):
                text = "".join(t.text or "" for t in node.findall(".//a:t", NS)).strip()
                if not text:
                    continue
                xfrm = node.find(".//a:xfrm", NS)
                if xfrm is None:
                    continue
                off = xfrm.find("a:off", NS)
                ext = xfrm.find("a:ext", NS)
                if off is None or ext is None:
                    continue
                c_nv_pr = node.find(".//p:cNvPr", NS)
                name = c_nv_pr.attrib.get("name", "") if c_nv_pr is not None else ""
                boxes.append(
                    TextBox(
                        slide=slide,
                        name=name or "text",
                        x=emu_to_in(off.attrib.get("x")),
                        y=emu_to_in(off.attrib.get("y")),
                        w=emu_to_in(ext.attrib.get("cx")),
                        h=emu_to_in(ext.attrib.get("cy")),
                        text=text,
                        font_size=font_size_pt(node),
                    )
                )
    return boxes


def estimate_lines(text: str, width_in: float, font_size_pt: float) -> int:
    # Approximate Chinese glyph width at 0.52em and Latin at 0.42em.
    # 1 pt = 1/72 inch. Use a conservative usable width after text margins.
    usable_w = max(0.1, width_in - 0.12)
    zh = sum(1 for ch in text if "\u4e00" <= ch <= "\u9fff")
    other = max(0, len(text) - zh)
    avg_char_in = (font_size_pt / 72) * ((zh * 0.52 + other * 0.42) / max(1, zh + other))
    chars_per_line = max(1, int(usable_w / max(0.03, avg_char_in)))
    explicit_lines = text.count("\n") + 1
    wrapped_lines = math.ceil(len(text.replace("\n", "")) / chars_per_line)
    return max(explicit_lines, wrapped_lines)


def inspect(pptx: Path, threshold: float) -> list[str]:
    warnings: list[str] = []
    for box in read_text_boxes(pptx):
        if box.w <= 0.05 or box.h <= 0.05:
            continue
        estimated = estimate_lines(box.text, box.w, box.font_size)
        line_height_in = box.font_size * 1.18 / 72
        needed_h = estimated * line_height_in + 0.10
        ratio = needed_h / max(0.01, box.h)
        if ratio >= threshold:
            preview = box.text.replace("\n", " ")[:42]
            warnings.append(
                f"{box.slide}: {box.name} likely dense text ratio={ratio:.2f} "
                f"font={box.font_size:.1f}pt box=({box.w:.2f}x{box.h:.2f}) text='{preview}'"
            )
    return warnings


def main() -> None:
    parser = argparse.ArgumentParser(description="Heuristic PPTX text fit preflight.")
    parser.add_argument("pptx", help="PPTX file to inspect.")
    parser.add_argument("--threshold", type=float, default=0.92, help="Warn when estimated needed height / box height exceeds this ratio.")
    args = parser.parse_args()

    warnings = inspect(Path(args.pptx), args.threshold)
    if not warnings:
        print("text_fit_guard: no likely text fit issues found")
        return
    print(f"text_fit_guard: {len(warnings)} likely text fit issue(s)")
    for warning in warnings:
        print("-", warning)


if __name__ == "__main__":
    main()
