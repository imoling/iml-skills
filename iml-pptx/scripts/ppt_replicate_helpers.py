"""Small PPT OOXML helpers for image-to-editable-PPT replication.

These helpers are intentionally low level. They provide stable editable shape,
text, line and picture XML for simple one-slide PPTX builders while leaving the
actual page layout decisions to the agent.
"""

from __future__ import annotations

import xml.etree.ElementTree as ET
from typing import List, Optional, Tuple


NS = {
    "p": "http://schemas.openxmlformats.org/presentationml/2006/main",
    "a": "http://schemas.openxmlformats.org/drawingml/2006/main",
    "r": "http://schemas.openxmlformats.org/officeDocument/2006/relationships",
}
for prefix, uri in NS.items():
    ET.register_namespace(prefix, uri)

EMU = 914400
SLIDE_W, SLIDE_H = 13.333333, 7.5
DEFAULT_FONT = "PingFang SC"


def qn(tag: str) -> str:
    prefix, local = tag.split(":")
    return f"{{{NS[prefix]}}}{local}"


def el(tag: str, attrs: Optional[dict] = None, children: Optional[List[ET.Element]] = None, text: Optional[str] = None) -> ET.Element:
    node = ET.Element(qn(tag), attrs or {})
    if text is not None:
        node.text = text
    for child in children or []:
        node.append(child)
    return node


def emu(value: float) -> str:
    return str(int(round(value * EMU)))


def px_x(px: float, image_width: float = 1672, slide_width: float = SLIDE_W) -> float:
    return px / image_width * slide_width


def px_y(px: float, image_height: float = 941, slide_height: float = SLIDE_H) -> float:
    return px / image_height * slide_height


def text_run(text: str, font_size: float, color: str, bold: bool = False, font: str = DEFAULT_FONT) -> ET.Element:
    rpr = el("a:rPr", {"lang": "zh-CN", "sz": str(int(font_size * 100)), "b": "1" if bold else "0"})
    rpr.append(el("a:solidFill", children=[el("a:srgbClr", {"val": color})]))
    rpr.append(el("a:latin", {"typeface": font}))
    rpr.append(el("a:ea", {"typeface": font}))
    return el("a:r", children=[rpr, el("a:t", text=text)])


def shape_xml(
    id_: int,
    x: float,
    y: float,
    w: float,
    h: float,
    text: str = "",
    fill: str = "none",
    line: str | None = None,
    radius: bool = False,
    font_size: float = 16,
    color: str = "111827",
    bold: bool = False,
    align: str = "l",
    valign: str = "mid",
) -> ET.Element:
    sp = el("p:sp")
    sp.append(el("p:nvSpPr", children=[el("p:cNvPr", {"id": str(id_), "name": f"Shape {id_}"}), el("p:cNvSpPr"), el("p:nvPr")]))
    sp_pr = el("p:spPr", children=[
        el("a:xfrm", children=[el("a:off", {"x": emu(x), "y": emu(y)}), el("a:ext", {"cx": emu(w), "cy": emu(h)})]),
        el("a:prstGeom", {"prst": "roundRect" if radius else "rect"}, children=[el("a:avLst")]),
    ])
    sp_pr.append(el("a:noFill") if fill == "none" else el("a:solidFill", children=[el("a:srgbClr", {"val": fill})]))
    sp_pr.append(el("a:ln", children=[el("a:noFill")]) if line is None else el("a:ln", {"w": "14000"}, children=[el("a:solidFill", children=[el("a:srgbClr", {"val": line})])]))
    sp.append(sp_pr)

    if text:
        anchor = {"top": "t", "mid": "ctr", "bottom": "b"}.get(valign, "ctr")
        body = el("p:txBody", children=[el("a:bodyPr", {"wrap": "square", "anchor": anchor}, children=[el("a:normAutofit")]), el("a:lstStyle")])
        for para in str(text).split("\n"):
            p = el("a:p")
            p.append(el("a:pPr", {"algn": align}))
            p.append(text_run(para, font_size, color, bold))
            body.append(p)
        sp.append(body)
    return sp


def line_xml(id_: int, x1: float, y1: float, x2: float, y2: float, color: str = "0057C8", width: float = 2, dash: bool = False) -> ET.Element:
    x, y = min(x1, x2), min(y1, y2)
    w, h = abs(x2 - x1) or 0.01, abs(y2 - y1) or 0.01
    ln_children = [el("a:solidFill", children=[el("a:srgbClr", {"val": color})])]
    if dash:
        ln_children.append(el("a:prstDash", {"val": "dash"}))
    sp = el("p:sp")
    sp.append(el("p:nvSpPr", children=[el("p:cNvPr", {"id": str(id_), "name": f"Line {id_}"}), el("p:cNvSpPr"), el("p:nvPr")]))
    sp.append(el("p:spPr", children=[
        el("a:xfrm", children=[el("a:off", {"x": emu(x), "y": emu(y)}), el("a:ext", {"cx": emu(w), "cy": emu(h)})]),
        el("a:prstGeom", {"prst": "line"}, children=[el("a:avLst")]),
        el("a:ln", {"w": str(int(width * 12700))}, children=ln_children),
    ]))
    return sp


def pic_xml(id_: int, rid: str, name: str, x: float, y: float, w: float, h: float) -> ET.Element:
    pic = el("p:pic")
    pic.append(el("p:nvPicPr", children=[
        el("p:cNvPr", {"id": str(id_), "name": name}),
        el("p:cNvPicPr", children=[el("a:picLocks", {"noChangeAspect": "1"})]),
        el("p:nvPr"),
    ]))
    pic.append(el("p:blipFill", children=[el("a:blip", {qn("r:embed"): rid}), el("a:stretch", children=[el("a:fillRect")])]))
    pic.append(el("p:spPr", children=[
        el("a:xfrm", children=[el("a:off", {"x": emu(x), "y": emu(y)}), el("a:ext", {"cx": emu(w), "cy": emu(h)})]),
        el("a:prstGeom", {"prst": "rect"}, children=[el("a:avLst")]),
    ]))
    return pic


def rels_xml(rels: List[Tuple[str, str, str]]) -> bytes:
    root = ET.Element("Relationships", {"xmlns": "http://schemas.openxmlformats.org/package/2006/relationships"})
    for rid, typ, target in rels:
        ET.SubElement(root, "Relationship", {"Id": rid, "Type": typ, "Target": target})
    return ET.tostring(root, encoding="utf-8", xml_declaration=True)
