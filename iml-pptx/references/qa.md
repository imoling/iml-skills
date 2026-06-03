# QA And Repair

Use this reference before reporting any generated, repaired or replicated PPT/PPTX page as complete.

## Mandatory Screenshot QA

For every editable PPT page:

1. Produce a screenshot preview of the PPT page.
2. Inspect the screenshot visually.
3. If only one page changed, preview that changed page.
4. If the available preview tool only renders the first slide, create a temporary one-slide preview for the changed page or use another renderer.
5. Run `python3 scripts/layout_guard.py` when possible to catch likely overlaps before visual QA.
6. Run `python3 scripts/connector_guard.py` when connector lines are present, especially overview, process or hub-and-spoke pages.
7. Compare screenshot against the source image.
8. Only report completion after preview has been produced and inspected.

Codex desktop preview command:

```bash
scripts/preview_pptx.sh output/deck.pptx output/preview
```

## Inspect For

- text overlap;
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

## Repair Order

1. Fix the grid: align cards by row/column and normalize gutters.
2. Fix text boxes: widen boxes, lower font size slightly, or add line breaks.
3. Fix labels and badges: move into card header or reserve a separate label row.
4. Fix connectors: route through gutters, reduce width, put behind cards, or switch connector type.
5. Fix icon sizes and image crops last.

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
