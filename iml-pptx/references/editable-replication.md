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

## Build Order

1. Background bands and decorative lines.
2. Cards, tables and containers.
3. Connector lines after card positions are locked.
4. Icons/images.
5. Text.
6. Intentionally floating labels/badges only after reserving their anchor area.

## Layout Safety

- Keep line width conservative; thick lines should not cross content modules.
- When a line must cross a region, send it behind opaque cards and keep text above it.
- Connector endpoints must attach to card edges or center-node edges, not arbitrary points inside text areas.
- Prefer lines with explicit anchor pairs: `from_card.edge -> to_card.edge`.
- If a page needs a route/trend line, verify it does not cross text at preview size.
- Create a connector manifest when a page has more than two lines.
- Create an icon manifest when a page has more than four icons.

## When To Pause For Confirmation

If a page is complex, visually ambiguous, screenshot-heavy, or likely to set the style for the rest of the deck, do one page first and ask the user to confirm before continuing. Once confirmed, continue the rest using the same logic.
