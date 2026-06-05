# Editable PPT Replication

Use this reference when converting page images, screenshots, photos or PDF pages into editable PPT/PPTX.

## Source Of Truth

- Replicate the existing page image.
- Do not redesign from scratch.
- Do not batch-generate generic slides that merely reuse the topic.
- Work page by page or in small visually similar batches.
- Preview each page and fix obvious errors before continuing.

## Editable Object Priorities

1. Text must be editable.
2. Boxes, cards, tables, lines, arrows, dividers and backgrounds should be editable.
3. Charts and diagrams should be recreated with editable PPT shapes where practical.
4. Icons and small logos may be high-quality image assets.
5. Photos, screenshots and generated bitmap visuals may be non-editable image assets, but captions, labels, callouts and frames should be editable.
6. When external visuals were collected, embed them into relevant PPT pages; do not leave them only as downloaded assets or notes.
7. For brand marks or small logos, prefer official/vector-like assets or clean library approximations. Avoid blurry screenshot crops unless exact identity matters more than vector clarity.

## Practical Rules

- Use source image coordinates when possible.
- Keep slide size 16:9, usually 13.333 x 7.5 inches.
- Keep page numbers and title chrome consistent.
- Use stable filenames with page numbers.
- Preserve source layout, hierarchy and information density.
- Use `PingFang SC` for Chinese and Latin text unless the source clearly uses another font.
- For dense tables, build editable rows/columns instead of one screenshot.
- For diagrams, recreate circles, arrows, cards and labels as PPT objects; insert icons as image assets if needed.
- For photo/screenshot-heavy pages, keep raster images as image assets and recreate labels, masks, frames and captions as editable objects.
- Avoid nesting UI-like cards inside unrelated cards unless the source image does so.
- Put decorative/guide lines behind cards; readable text must sit above all lines and shapes.
- Do not let arrows or connectors share the same layer as body text.
- Reserve explicit lanes for flows, arrows, tabs, badges and footnotes.
- Never flatten the whole slide as a screenshot just because it contains an image.
- Every text object inside a card, note band, table cell, badge, caption or callout must use the container's inner safe zone, not the visual container's outer bounds.
- Default text padding inside cards: left/right at least 0.14 in, top/bottom at least 0.10 in. Increase padding for large titles, Chinese body text, and orange/yellow note bands.
- A text box must be smaller than its parent container. Never let a body text box extend below a card and rely on visual overlap to look acceptable.
- If using `pptxgenjs`, set explicit `x/y/w/h` for the inner text zone and use `fit: "shrink"` or equivalent only as a backup. Autofit is not a layout strategy.

## Build Order

1. Background bands and decorative lines.
2. Cards, tables and containers.
3. Define inner text zones for every container.
4. Connector lines after card positions are locked.
5. Icons/images.
6. Text.
7. Intentionally floating labels/badges only after reserving their anchor area.

## Layout Safety

- For each card, calculate `text_x = card_x + padding`, `text_y = card_y + padding`, `text_w = card_w - 2*padding`, and `text_h = card_h - title/icon/reserved areas - padding`.
- Keep body copy short enough for the reserved text zone. If the source image shows dense copy, either enlarge the card or reduce the copy; do not spill outside the card.
- For cards with icons, reserve icon lanes first, then start text after the icon lane.
- For note bands and audience boxes, vertically center only after confirming the text fits in the band height.
- Keep line width conservative; thick lines should not cross content modules.
- When a line must cross a region, send it behind opaque cards and keep text above it.
- Connector endpoints must attach to card edges or center-node edges, not arbitrary points inside text areas.
- Prefer lines with explicit anchor pairs: `from_card.edge -> to_card.edge`.
- If a page needs a route/trend line, verify it does not cross text at preview size.
- Create a connector manifest when a page has more than two lines.
- Create an icon manifest when a page has more than four icons.

## When To Pause For Confirmation

If a page is complex, visually ambiguous, screenshot-heavy, or likely to set the style for the rest of the deck, do one page first and ask the user to confirm before continuing. Once confirmed, continue the rest using the same logic.
