---
name: paint-beyond-the-frame
description: Transform a user-supplied real photograph into a wide mixed-media artwork that preserves the photo as an undistorted factual panel and extends beyond its right edge into a softly colored imagined scene from the same place, time, scale, weather, and emotional world. Use for 镜外生境、照片向右扩画布、彩色想象续写、真实摄影加低饱和水彩或彩铅场景、同一世界的画外延伸、彩色摄影插画拼贴，尤其当用户要求保留原图、不复制主体、有色彩、有空气感、少文字和自然留白时。Do not use for ordinary photo retouching, background replacement, black-and-white sketch conversion, exact panorama reconstruction, or unrelated fantasy scenes.
---

# 镜外生境 · Paint Beyond the Frame

Create one continuous world across two media:

- keep the photograph factual, intact, and recognizable;
- let the canvas grow to the right instead of squeezing the source;
- invent what could exist just beyond the camera frame;
- render the invented area with restrained color, light, weather, and paper texture;
- preserve semantic continuity without copying exact shapes.

Treat color as structural, not decorative. The imagined side must feel alive and atmospheric, not like a black-and-white draft.

Return the finished image with one brief Chinese creative rationale. Do not expose internal analysis unless the user asks.

## Priority Order

Resolve conflicts in this order:

1. Preserve the source photo's native proportions, perspective, identity, and recognizable details.
2. Keep the primary subject unique; do not create an illustrated duplicate.
3. Continue the same world rather than inventing an unrelated metaphor or location.
4. Preserve color atmosphere on the imagined side.
5. Balance visual weight, depth, density, and negative space.
6. Keep the seam narrow and the mixed-media character tactile.
7. Add text only when it improves the composition.

## Consent and Handling

- Treat a supplied photo plus a transformation request as consent to edit it; do not ask again.
- Send only the required image and final prompt to the image-generation service.
- Do not browse for, publish, or store the source outside the active task.
- Do not place source or generated images inside this skill directory.

## 1. Read the Source

Build an internal Scene Card:

- **Anchor subject:** the subject that must stay photographic and unique.
- **World:** interior, street, forest, garden, coast, mountain, habitat, exhibition, or other place logic.
- **Spatial rules:** eye height, horizon family, perspective, depth layers, path, slope, enclosure, and movement direction.
- **Materials:** foliage, soil, stone, timber, concrete, water, glass, textile, haze, or light.
- **Time and air:** season, weather, light direction, color temperature, humidity, mist, and atmosphere.
- **Visual weight:** faces, saturated regions, dark masses, open areas, edge tension, and texture density.
- **Continuation vocabulary:** 3–6 source-supported elements that could plausibly appear just beyond the right edge.
- **Forbidden repeats:** the person, animal, landmark, silhouette, or arrangement that must not reappear.

Write one internal Continuation Thesis:

> If the camera moved right without changing place or time, it could reveal [one new spatial development] with [2–4 restrained elements].

Do not generate until this sentence describes a coherent scene rather than a list of objects.

## 2. Derive a Color Script

Extract 3–5 color roles from the source rather than selecting arbitrary colors:

- one atmospheric base: sky, haze, wall, water, or shadow;
- one environmental midtone: foliage, earth, timber, stone, or architecture;
- one warm or cool counterpoint;
- optionally one restrained accent already supported by the photo;
- one paper or highlight tone.

Apply the palette by role:

- make the imagined side slightly lighter, softer, and less saturated than the photograph;
- preserve the source's light direction and color temperature;
- use diluted watercolor washes, colored pencil, dry pastel, or translucent gouache;
- use dark brown, gray-blue, moss green, plum-gray, or another palette-derived dark for linework;
- reserve pure black for rare emphasis only;
- keep some paper visible inside colored areas so the right side remains visibly imagined;
- let one or two source colors cross the seam as pigment, not as copied objects.

Do not allow the right side to collapse into monochrome unless the user explicitly requests it. Do not make it equally photographic or glossy.

## 3. Protect and Extend the Photograph

### Non-negotiable invariants

- Keep the full source at its native aspect ratio.
- Never squeeze, stretch, narrow, widen, repaint, re-pose, or rearrange the source.
- Add space by extending the canvas to the right.
- Keep faces, bodies, animals, architecture, and defining objects outside the transition band.
- Preserve the original photographic grain, depth, color, and optical character.

### Deterministic local workflow

When the source has a local path, use `scripts/protect_photo_extension.py`.

Prepare a right-extension canvas and palette manifest:

```bash
python scripts/protect_photo_extension.py prepare \
  --source <source-image> \
  --output <prepared-canvas.png> \
  --manifest <layout.json>
```

Inspect the prepared canvas. Use it as the edit target and instruct image generation to change only the paper extension and the narrow seam.

After generation, restore the protected source pixels:

```bash
python scripts/protect_photo_extension.py restore \
  --source <source-image> \
  --generated <generated-image> \
  --manifest <layout.json> \
  --output <final-image.png>
```

Verify the protected region:

```bash
python scripts/protect_photo_extension.py verify \
  --source <source-image> \
  --final <final-image.png> \
  --manifest <layout.json>
```

If the source exists only in the conversation, edit it with the same locked-panel constraints. Do not claim pixel-perfect preservation; inspect the result and make one targeted correction if needed.

## 4. Choose the Canvas

Use these starting points, then adjust by visual weight:

| Source | Total output width | Approximate photo share |
|---|---:|---:|
| Landscape | 1.45–1.75× source width | 57–69% |
| Square | 1.65–1.90× source width | 53–61% |
| 4:5 or 3:4 portrait | 1.80–2.05× source width | 49–56% |
| 9:16 portrait | 1.85–2.00× source width | 50–54% |

Never force a mechanical 50/50 split. Preserve the complete source first. Keep the transition band about 4–7% of source width and away from the anchor subject.

## 5. Invent the Scene Beyond the Frame

### Inherit

Preserve:

- place type and environmental logic;
- time, season, weather, light direction, and air quality;
- eye height, perspective family, spatial scale, and depth rhythm;
- material vocabulary, surface age, and emotional temperature;
- one or two directional gestures from the photograph.

### Transform

Introduce:

- a genuinely new arrangement of space;
- 2–4 plausible elements from the Continuation vocabulary;
- new silhouettes, intervals, and overlaps;
- one subtle narrative invitation, such as a path continuing, light opening, traces of activity, or a quieter layer of depth.

Translate the eye path, not exact contours. A path may become an invitation; gaze may become open space; wind may become pigment flow; depth may become layered translucent washes.

### Forbid

Never:

- duplicate the anchor person, animal, building, artwork, or landmark;
- trace the photo as line art;
- extend the exact ridge, skyline, wall, branch, or silhouette;
- turn a source object into a giant close-up, diagram, specimen, or cross-section;
- jump to an unrelated location, dream symbol, or fantasy genre;
- add a second focal subject equal to the photographic anchor;
- scatter disconnected objects, thumbnails, labels, or decorative filler;
- fill every gap merely because space exists.

## 6. Shape the Colored Imagined Side

Make the right side a complete painted scene rather than a decorated blank field.

- Keep its information density slightly below the photographic side.
- Reserve about 25–45% of the illustrated field as breathing room, including softly washed paper.
- Use one modest scene cluster, one supporting directional gesture, and at most one sparse texture field.
- Simplify dense foliage, gravel, crowds, wire, or fur into grouped colored masses and broken rhythms.
- Let marks and saturation become quieter toward the outer edge.
- Use imperfect edges, pigment blooms, pencil interruptions, dry-brush gaps, paper fibers, and slight registration shifts.
- Avoid polished vector lines, cute cartoon rendering, anime styling, glossy 3D depth, heavy black hatching, or photorealistic outpainting.

The right side should have weather, light, and atmosphere. It may be dreamlike, but it must still obey the source world's physical logic.

## 7. Blend the Seam

- Keep the source visible as a clean photographic rectangle.
- Blend only the final 4–7% near its right edge.
- Use paper fiber, pigment loss, diluted color, faint pencil, or one to three crossing gestures.
- Do not melt, crop, repaint, or obscure the anchor subject.
- Make color drift from the photo into the imagined side before shapes do.

## 8. Handle Text

Default to no text. Add one tiny line only when a natural quiet area exists and the user wants a more editorial feeling.

- Use 1–5 words.
- Preserve supplied wording verbatim.
- Keep it subordinate, imperfect, and integrated into the paper.
- Omit it if it becomes a third focal point.
- Never invent dates, locations, coordinates, quotations, serial numbers, or metadata.

## 9. Compile the Generation Prompt

Write the image prompt in five compact sections:

1. **Canvas and edit target:** define the locked left photo and adaptive rightward extension.
2. **Source invariants:** state exactly what must remain unchanged and unique.
3. **Beyond-frame scene:** give the Continuation Thesis, inherited world rules, new elements, scale, and negative space.
4. **Color and material:** give the 3–5 color roles, pigment media, line colors, light, air, paper, and narrow seam.
5. **Hard avoids:** forbid distortion, duplicate subjects, contour tracing, monochrome default, photorealistic right side, unrelated scenery, clutter, text noise, logos, and watermarks.

Use concrete, pixel-visible language. Do not include file paths, analysis labels, or design-theory explanations in the generation prompt.

## 10. Generate and Correct

1. Inspect the source.
2. Build the Scene Card, Continuation Thesis, and Color Script.
3. Choose the canvas width and seam position.
4. Prepare a protected canvas when a local path exists.
5. Generate one image at a time.
6. Restore and verify the photographic pixels when using the local workflow.
7. Inspect at normal size and thumbnail size.
8. Apply the Quality Gate.
9. Regenerate once with one targeted correction when needed.
10. Return the image and a concise rationale.

Target only the observed failure:

- **Photo changed:** restore the original panel and widen the canvas instead of shrinking it.
- **Seam invaded the subject:** narrow or move the seam to a quieter edge.
- **Duplicate subject:** remove it and replace it with environmental evidence or activity traces.
- **Right side copied shapes:** rebuild the spatial arrangement with new silhouettes.
- **Right side feels unrelated:** restore place, time, perspective, materials, and source-supported vocabulary.
- **Right side is monochrome or dead:** reintroduce the Color Script through translucent washes, colored linework, light, and air.
- **Right side looks photographic:** expose paper, simplify forms, break edges, and reduce local detail.
- **Right side is too loud:** reduce saturation, dark mass, and object scale; increase washed breathing room.
- **Right side is too empty:** add one coherent scene cluster, not scattered filler.
- **Text distracts:** remove it.

## Quality Gate

Before returning, verify:

- Is the complete source photo preserved at natural proportions?
- Is the protected source region unchanged when the deterministic workflow is available?
- Does the anchor subject remain intact and unique?
- Was space added to the right instead of taken from the photo?
- Does the continuation belong to the same place, time, weather, perspective, scale, and emotional world?
- Is it a new scene rather than a traced or repeated version of the source?
- Are the new elements plausible and restrained?
- Does the imagined side clearly contain source-derived color, light, weather, and air?
- Is it visibly painted or drawn rather than photorealistic?
- Is the color softer than the photo but still alive?
- Is visual weight balanced at thumbnail size?
- Is the seam narrow, tactile, and outside the defining subject?
- Is negative space intentional rather than unfinished?
- Is text omitted unless genuinely useful?
- Does the result read as one world extending beyond the camera frame?
