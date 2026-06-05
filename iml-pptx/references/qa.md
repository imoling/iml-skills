# QA And Repair

Use this reference before reporting any generated, repaired or replicated PPT/PPTX page as complete.

## Mandatory Screenshot QA

For every editable PPT page:

1. Produce a screenshot preview of the PPT page.
2. Inspect the screenshot visually.
3. If only one page changed, preview that changed page.
4. If the available preview tool only renders the first slide, create a temporary one-slide preview for the changed page or use another renderer.
5. Run `python3 scripts/layout_guard.py` when possible to catch likely overlaps before visual QA.
6. Run `python3 scripts/text_fit_guard.py` when possible to catch likely text-density and text-box fit issues.
7. Run `python3 scripts/connector_guard.py` when connector lines are present, especially overview, process or hub-and-spoke pages.
8. Compare screenshot against the source image.
9. Only report completion after preview has been produced and inspected.

Codex desktop preview command:

```bash
scripts/preview_pptx.sh output/deck.pptx output/preview
```

## Inspect For

- text overlap;
- text escaping its card, table cell, note band, callout, caption frame or badge;
- tag/badge overlap with card borders or text;
- clipped text or bad wrapping;
- missing icons;
- blank SVG/image boxes;
- irrelevant or low-quality images;
- image crop hiding the important subject;
- image layer covering editable content;
- incorrect page number;
- major layout drift;
- wrong font;
- dense tables crossing grid lines;
- connectors or diagonal lines crossing important text;
- connectors entering card interiors instead of card edges;
- decorative slash lines without relationship meaning;
- cards in the same row not sharing top/bottom alignment;
- inconsistent gutters or too-small spacing.
- text boxes whose bottom edge extends below the intended container even if the text is not clipped.

## Repair Order

1. Fix the grid: align cards by row/column and normalize gutters.
2. Fix text containment: move text boxes inside the container safe zone and ensure bottom/right edges stay inside the card or band.
3. Fix copy density: shorten copy, add line breaks, widen boxes, increase container height, or lower font size slightly.
4. Fix labels and badges: move into card header or reserve a separate label row.
5. Fix connectors: route through gutters, reduce width, put behind cards, or switch connector type.
6. Fix icon sizes and image crops last.

## Text Containment QA

For each editable card/table/callout/band:

1. Identify the visible container boundary.
2. Identify the actual editable text box boundary.
3. Confirm text starts after the reserved icon/title lane.
4. Confirm text box bottom and right edges stay inside the container with padding.
5. Confirm the rendered text itself does not visually escape the container after line wrapping.

Common repairs:

- Body paragraph escapes below a card: shorten copy or increase card height before lowering font size.
- Text sits inside the text box but outside the visible card: recompute text box `y/h` from the card inner bounds.
- Note-band copy spills below the band: raise band height or split into two lines with a smaller font.
- Dense cards in a grid overflow: reduce cards per row or switch the page to a table/summary layout.

## Image Repair

When images feel decorative or distracting:

1. Remove the image if it does not explain the page.
2. Replace generic image with a specific scenario/product/industry visual.
3. Reduce image size or move it into a right panel/screenshot card.
4. Add opaque content cards if text sits over an image.
5. Keep captions/callouts editable; do not flatten them into the image.

## Common Failure Modes

- Generating a nice but different PPT instead of replicating the image.
- Treating a source image as loose inspiration.
- Using low-resolution cropped icons when a clear icon-library substitute is better.
- Hand-drawing icons that look inconsistent with the deck.
- Embedding SVGs without previewing; some preview/render paths show blank boxes.
- Forgetting `PingFang SC` after the user asks for 苹果苹方.
- Batch-producing many pages without visual QA.
- Reporting completion before rendering previews.
- Replacing dense original pages with simplified layouts unless the user asks for simplification.
- Letting editable text boxes extend outside their visual cards or note bands.
