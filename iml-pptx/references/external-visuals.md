# External Visuals

Use this reference whenever the deck/page mentions a concrete public product, software, SaaS/app/platform, website URL, company, public person, place, device, object, UI or real-world environment and a real visual would make the PPT more useful.

## Acquisition Gate

Required behavior:

1. Proactively browse, search images, inspect official pages, or capture screenshots before designing the slide unless the user forbids internet use or the entity is private/sensitive/inaccessible.
2. Product/software/platform decks should collect official or verified visuals when available: homepage, workbench, feature UI, docs, app listing, login/onboarding, settings, connector/permission pages, task workflow, result/output state, pricing/comparison page, or release notes.
3. URL-based decks should open/fetch the URL, capture relevant page screenshots, extract usable logos/product screenshots, and use those assets as PPT evidence or walkthrough visuals.
4. Public-person decks should prefer official bio pages, press kits, company profiles, Wikimedia/Wikipedia-compatible assets, or verified public sources. For private/non-public people, request user-provided images or permission.
5. Save acquired visuals in the project asset folder and maintain an asset/source manifest such as `assets/source_manifest.json`.
6. Put selected visuals into the PPT as screenshot cards, visual panels, walkthrough strips, thumbnails or background washes. Do not leave them only as notes or prompt references.
7. If browsing/screenshot tools are unavailable, record the constraint and use the best fallback: user-provided images, existing local assets, icon-library assets, or generated images.
8. Use generated images only when real/verified visuals are unavailable, inaccessible, low quality, inappropriate, or would expose private/sensitive data.

## Manifest Fields

Use this shape when practical:

```json
{
  "local_path": "assets/source/example.png",
  "source_url": "https://example.com/page",
  "source_type": "official_docs | official_site | screenshot | user_provided | generated | verified_public",
  "why_used": "what this visual proves or clarifies",
  "target_slide": "P03",
  "placement": "right visual panel | screenshot card | callout rail | thumbnail grid | background wash",
  "crop_notes": "what was cropped and why"
}
```

## When To Use Images

Use image assets when:

- `案例页`: show the company/product/system/site/context.
- `场景页`: show workplace, industry scene, user journey, interface or operational environment.
- `封面/章节页`: use one strong thematic image as mood and context.
- `产品/平台页`: use screenshot, product UI, device, architecture mockup or platform visual.
- `安装/上手页`: show official installer, login, first-run, workspace or entry-point screenshots.
- `操作流程页`: use screenshots for key UI states when teaching a product workflow; keep arrows, labels, step numbers, callouts and captions editable.
- `结果验收页`: show the actual output/result/preview area.
- `权限/连接器/自动化页`: show actual settings, connector, authorization, sidebar or task-management UI.
- `行业页`: use industry-specific imagery such as factory, grid, railway, port, hospital, office or retail store.
- `总结/建议页`: use a small symbolic image only if it strengthens the final judgment.

Avoid image assets when:

- `数据页`: numbers/evidence need priority.
- `密集表格页`: images usually create noise; use group header icons instead.
- Generic process pages where diagrams/icons explain the sequence better than screenshots.
- The image is generic, decorative, dark, blurry, over-cropped or unrelated.

## Placement Patterns

- `Right visual panel`: image on the right, editable claims/modules on the left.
- `Top strip`: narrow image band under the title for scene context.
- `Background wash`: low-contrast image with opaque white content cards; use sparingly.
- `Screenshot card`: screenshot framed as evidence, with editable callouts.
- `Screenshot walkthrough`: 2-4 screenshot cards arranged as a step sequence.
- `Screenshot + callout rail`: large screenshot with 3-5 editable numbered callouts.
- `Case thumbnail grid`: small image thumbnails with editable labels and metrics.
- `Hero image + overlays`: cover/section pages only; avoid for dense content pages.

## Image QA

Ask:

- Would removing this image weaken the page?
- Does it reveal the actual scenario/product/object, not just mood?
- For product decks, would a new user know where the feature lives after seeing the slide?
- Is it official/user-provided/verified and free of sensitive private data?
- Are captions and callouts editable PPT objects rather than flattened into the image?
- Are important words, numbers and table cells still editable and readable?
- Is the crop clean and consistent with the page grid?
- Does the image compete with the title or core conclusion?
