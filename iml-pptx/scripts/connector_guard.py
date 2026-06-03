#!/usr/bin/env python3
"""Scan PPTX line shapes for accidental or unstable connectors."""

from __future__ import annotations

import argparse
import re
import sys
import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET


NS = {
    "p": "http://schemas.openxmlformats.org/presentationml/2006/main",
    "a": "http://schemas.openxmlformats.org/drawingml/2006/main",
}
EMU_PER_INCH = 914400
SLIDE_RE = re.compile(r"ppt/slides/slide(\d+)\.xml$")


def scan_lines(
    pptx_path: Path, threshold: float, allowed_slides: set[int]
) -> tuple[list[tuple[int, float, float]], list[tuple[int, float, float]]]:
    diagonal_issues: list[tuple[int, float, float]] = []
    negative_extent_issues: list[tuple[int, float, float]] = []
    with zipfile.ZipFile(pptx_path) as zf:
        slides: list[tuple[int, str]] = []
        for name in zf.namelist():
            match = SLIDE_RE.match(name)
            if match:
                slides.append((int(match.group(1)), name))

        for slide_no, name in sorted(slides):
            root = ET.fromstring(zf.read(name))
            for shape in root.findall(".//p:sp", NS):
                geom = shape.find(".//a:prstGeom", NS)
                if geom is None or geom.attrib.get("prst") != "line":
                    continue
                ext = shape.find(".//a:ext", NS)
                if ext is None:
                    continue
                raw_width = int(ext.attrib.get("cx", "0")) / EMU_PER_INCH
                raw_height = int(ext.attrib.get("cy", "0")) / EMU_PER_INCH
                width = abs(raw_width)
                height = abs(raw_height)
                if raw_width < 0 or raw_height < 0:
                    negative_extent_issues.append((slide_no, round(raw_width, 3), round(raw_height, 3)))
                if slide_no not in allowed_slides and width > threshold and height > threshold:
                    diagonal_issues.append((slide_no, round(width, 3), round(height, 3)))
    return diagonal_issues, negative_extent_issues


def main() -> int:
    parser = argparse.ArgumentParser(description="Detect likely accidental or unstable PPT connector lines.")
    parser.add_argument("pptx", type=Path)
    parser.add_argument("--threshold", type=float, default=0.03, help="minimum width and height in inches")
    parser.add_argument(
        "--allow-slide",
        type=int,
        action="append",
        default=[],
        help="slide number with intentional diagonal relation/trend lines; can be repeated",
    )
    args = parser.parse_args()

    allowed_slides = set(args.allow_slide)
    diagonal_issues, negative_extent_issues = scan_lines(args.pptx, args.threshold, allowed_slides)
    if not diagonal_issues and not negative_extent_issues:
        if allowed_slides:
            allowed = ", ".join(f"P{s}" for s in sorted(allowed_slides))
            print(f"connector_guard: no unexpected diagonal-like line shapes found; allowed slides: {allowed}")
        else:
            print("connector_guard: no diagonal-like line shapes found")
        return 0

    if diagonal_issues:
        print(f"connector_guard: {len(diagonal_issues)} diagonal-like line shape(s)")
        for slide_no, width, height in diagonal_issues:
            print(f"- P{slide_no}: w={width}in h={height}in")
    if negative_extent_issues:
        print(f"connector_guard: {len(negative_extent_issues)} line shape(s) with negative extents")
        for slide_no, width, height in negative_extent_issues:
            print(f"- P{slide_no}: cx={width}in cy={height}in")
        print("  Fix: use positive width/height and flipH/flipV instead of negative cx/cy.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
