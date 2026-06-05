#!/usr/bin/env python3
"""Heuristic PPTX layout overlap checker.

This script parses slide XML and reports likely large bounding-box overlaps.
It is designed as a cheap preflight before visual preview. It cannot know which
overlaps are intentional, so warnings should be inspected rather than treated as
automatic failures.
"""

from __future__ import annotations

import argparse
import math
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
class Box:
    slide: str
    kind: str
    name: str
    x: float
    y: float
    w: float
    h: float
    has_text: bool

    @property
    def area(self) -> float:
        return max(0.0, self.w) * max(0.0, self.h)

    @property
    def is_line_like(self) -> bool:
        return min(self.w, self.h) <= 0.04 and max(self.w, self.h) >= 0.2


def emu_to_in(value: str | None) -> float:
    if not value:
        return 0.0
    return int(value) / EMU_PER_INCH


def get_text(node: ET.Element) -> str:
    return "".join(t.text or "" for t in node.findall(".//a:t", NS)).strip()


def read_boxes(pptx: Path) -> list[Box]:
    boxes: list[Box] = []
    with zipfile.ZipFile(pptx) as zf:
        slide_names = sorted(n for n in zf.namelist() if n.startswith("ppt/slides/slide") and n.endswith(".xml"))
        for slide in slide_names:
            root = ET.fromstring(zf.read(slide))
            for node in root.findall(".//p:sp", NS) + root.findall(".//p:pic", NS):
                xfrm = node.find(".//a:xfrm", NS)
                if xfrm is None:
                    continue
                off = xfrm.find("a:off", NS)
                ext = xfrm.find("a:ext", NS)
                if off is None or ext is None:
                    continue
                name = ""
                c_nv_pr = node.find(".//p:cNvPr", NS)
                if c_nv_pr is not None:
                    name = c_nv_pr.attrib.get("name", "")
                text = get_text(node)
                boxes.append(
                    Box(
                        slide=slide,
                        kind="pic" if node.tag.endswith("pic") else "shape",
                        name=name or node.tag.rsplit("}", 1)[-1],
                        x=emu_to_in(off.attrib.get("x")),
                        y=emu_to_in(off.attrib.get("y")),
                        w=emu_to_in(ext.attrib.get("cx")),
                        h=emu_to_in(ext.attrib.get("cy")),
                        has_text=bool(text),
                    )
                )
    return boxes


def overlap(a: Box, b: Box) -> tuple[float, float]:
    x1 = max(a.x, b.x)
    y1 = max(a.y, b.y)
    x2 = min(a.x + a.w, b.x + b.w)
    y2 = min(a.y + a.h, b.y + b.h)
    iw = max(0.0, x2 - x1)
    ih = max(0.0, y2 - y1)
    area = iw * ih
    if area <= 0:
        return 0.0, 0.0
    small = max(0.0001, min(a.area, b.area))
    large = max(0.0001, max(a.area, b.area))
    return area / small, area / large


def is_probably_background(box: Box, slide_w: float, slide_h: float) -> bool:
    return box.w >= slide_w * 0.85 and box.h >= slide_h * 0.85


def inspect(pptx: Path, min_area_ratio: float, include_containers: bool) -> list[str]:
    boxes = read_boxes(pptx)
    warnings: list[str] = []
    for i, a in enumerate(boxes):
        if is_probably_background(a, 13.333333, 7.5):
            continue
        for b in boxes[i + 1 :]:
            if a.slide != b.slide or is_probably_background(b, 13.333333, 7.5):
                continue
            if not include_containers:
                text_text = a.has_text and b.has_text
                line_text = (a.is_line_like and b.has_text) or (b.is_line_like and a.has_text)
                if not (text_text or line_text):
                    continue
            else:
                if not (a.has_text or b.has_text):
                    continue
            if a.has_text and b.has_text is False and not b.is_line_like and not include_containers:
                continue
            if b.has_text and a.has_text is False and not a.is_line_like and not include_containers:
                continue
            small_ratio, large_ratio = overlap(a, b)
            if small_ratio >= min_area_ratio and large_ratio >= min_area_ratio / 4:
                label = "LINE/TEXT" if a.is_line_like or b.is_line_like else ("TEXT" if a.has_text or b.has_text else "BOX")
                warnings.append(
                    f"{label} overlap {a.slide}: {a.name} ({a.kind}) vs {b.name} ({b.kind}) "
                    f"small={small_ratio:.2f} large={large_ratio:.2f}"
                )
    return warnings


def main() -> None:
    parser = argparse.ArgumentParser(description="Heuristic PPTX overlap preflight.")
    parser.add_argument("pptx", help="PPTX file to inspect.")
    parser.add_argument("--min-area-ratio", type=float, default=0.08, help="Minimum overlap ratio against smaller box.")
    parser.add_argument("--include-containers", action="store_true", help="Also report text overlapping non-line containers. Noisy, but useful when debugging badges over cards.")
    args = parser.parse_args()

    warnings = inspect(Path(args.pptx), args.min_area_ratio, include_containers=args.include_containers)
    if not warnings:
        print("layout_guard: no likely overlaps found")
        return
    print(f"layout_guard: {len(warnings)} likely overlap(s)")
    for warning in warnings:
        print("-", warning)


if __name__ == "__main__":
    main()
