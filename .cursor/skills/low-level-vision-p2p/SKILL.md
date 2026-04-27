---
name: low-level-vision-p2p
description: Converts a single input image into task-specific outputs for low-level vision and pixel-to-pixel transformations using frontier image generation models (e.g., GPT-Image). Use when users request denoise/deblur/super-resolution/dehaze/relight/depth/normals/edge/segmentation-like map generation or other pixel-to-pixel image transformation tasks from one source image.
---

# Low-Level Vision Pixel-to-Pixel

## Purpose

Given:
- one input image
- one task name

Produce:
- one transformed image aligned with low-level vision or pixel-to-pixel requirements

This skill standardizes:
- task taxonomy
- prompt templates
- automation workflow
- output naming and reproducibility

## Task Taxonomy

Use these canonical task IDs:

### Restoration
- `denoise`
- `deblur`
- `super_resolution`
- `jpeg_artifact_removal`
- `dehaze`
- `derain`
- `deweather` (snow/fog/rain blend cleanup)
- `low_light_enhance`
- `color_correction`
- `white_balance`
- `exposure_correction`
- `lens_distortion_correction`
- `vignette_removal`
- `reflection_removal`
- `shadow_removal`
- `moire_removal`

### Color and Tone Mapping
- `grayscale_to_color`
- `day_to_night`
- `night_to_day`
- `style_preserving_relight` (illumination only, geometry preserved)
- `hdr_like_tone_mapping`

### Geometry and View-Preserving Transforms
- `rectification` (document/building perspective correction)
- `inpainting_structural` (fill missing region with coherent local structure)
- `outpainting_local_context` (small context extension while preserving scene)

### Dense Prediction Style Outputs (Rendered as Images)
- `edge_map`
- `line_art_clean`
- `depth_map`
- `albedo_layer`
- `shading_layer`
- `surface_normals`
- `saliency_map`
- `binary_mask_foreground`
- `semantic_segmentation_map`

### Domain Translation (Pixel-Aligned Preference)
- `photo_to_sketch`
- `sketch_to_photo`
- `map_to_satellite_like`
- `satellite_like_to_map`
- `thermal_like_render`

## Prompt Contract

Always construct prompt with:
1. **Task intent**
2. **Hard constraints**
3. **Preservation constraints**
4. **Output format constraints**
5. **Failure avoidance**

Use this base template:

```text
You are performing a low-level vision pixel-to-pixel transformation.
Task: {task_id}

Input image is the only source of truth. Keep scene geometry, camera viewpoint, object identity, and composition unchanged unless task explicitly requires map rendering.

Primary objective:
{task_objective}

Hard constraints:
- No added or removed objects.
- No text, watermark, logo, or border.
- Keep global framing and perspective consistent with input.
- Preserve fine structures (hair, wires, edges, micro-texture) whenever compatible with the task.

Output specification:
{output_spec}

Quality bar:
{quality_bar}

If uncertain, prefer conservative edits over aggressive hallucination.
```

## Task-Specific Prompt Extensions

Append one extension by task:

- `denoise`: "Remove sensor and chroma noise while preserving true texture and edge sharpness. Avoid plastic smoothing."
- `deblur`: "Recover sharp details from motion/defocus blur while avoiding ringing and over-sharpening."
- `super_resolution`: "Increase perceived resolution and detail fidelity naturally. Do not invent new semantic content."
- `jpeg_artifact_removal`: "Remove blocking and ringing artifacts from JPEG compression, keep natural gradients."
- `dehaze`: "Reduce atmospheric haze/fog and restore contrast with realistic color and depth cues."
- `derain`: "Remove rain streaks and rain veil while preserving scene details and lighting."
- `deweather`: "Clean weather artifacts (rain/snow/fog) with minimal change to underlying scene."
- `low_light_enhance`: "Improve brightness and visibility in dark regions with controlled noise and realistic color."
- `color_correction`: "Correct color cast and restore natural tones while preserving material appearance."
- `white_balance`: "Neutralize illumination color cast and maintain realistic neutral surfaces."
- `exposure_correction`: "Balance highlights/shadows, recover details, avoid clipping."
- `lens_distortion_correction`: "Correct geometric distortion while preserving straight lines and proportions."
- `vignette_removal`: "Remove corner darkening smoothly, keep natural light falloff."
- `reflection_removal`: "Suppress glass reflections and reveal underlying scene content. Blurry or ghost layers are  reflection layer and need to be removed. The sharp and clear part are underlying part."
- `shadow_removal`: "Reduce cast shadows while keeping object boundaries and albedo realistic."
- `moire_removal`: "Suppress moire/interference patterns while retaining texture fidelity."
- `grayscale_to_color`: "Colorize grayscale image with plausible, coherent, natural colors."
- `style_preserving_relight`: "Relight illumination only; keep identity, texture, and geometry fixed."
- `rectification`: "Correct perspective to fronto-parallel where appropriate without cropping critical content."
- `inpainting_structural`: "Fill missing region consistently with nearby structure, texture, and lighting."
- `outpainting_local_context`: "Extend context locally with high consistency to existing scene."
- `edge_map`: "Output a clean high-contrast edge image, white edges on black background."
- `line_art_clean`: "Output simplified clean line drawing preserving major contours."
- `depth_map`: "Output relative depth map as grayscale: near bright, far dark, smooth but edge-aware."
- `albedo_layer`: "Output intrinsic albedo (reflectance) layer. Remove illumination effects and cast shadows as much as possible while preserving material colors."
- `shading_layer`: "Output intrinsic shading/illumination layer. Preserve light and shadow structure while suppressing reflectance/color patterns."
- `surface_normals`: "Output surface normal map in standard RGB normal encoding."
- `saliency_map`: "Output saliency heatmap-style image emphasizing visually important regions."
- `binary_mask_foreground`: "Output binary mask: foreground white, background black, clean boundaries."
- `semantic_segmentation_map`: "Output semantic segmentation color map with clearly separated classes."
- `photo_to_sketch`: "Convert photo to clean sketch while preserving structure and proportions."
- `sketch_to_photo`: "Render sketch into realistic photo while respecting original line geometry."

## Automation Workflow

1. Validate inputs:
   - `input_image` exists
   - `task_id` is canonical
2. Build final prompt from:
   - base template + task extension
3. Call image edit API with:
   - one source image
   - final prompt
4. Save output to:
   - `outputs/{task_id}/{input_basename}__{task_id}.png`
5. Write metadata JSON:
   - model
   - prompt
   - timestamp
   - task_id

## Default Parameters

- Model: `gpt-image-2` (configurable)
- Size: `1024x1024` (configurable)
- Format: `png`
- Determinism: best-effort via fixed prompt and config snapshot

## Usage Pattern

When user asks for low-level/pixel-to-pixel transform:
1. Map user phrase to canonical `task_id`.
2. If ambiguous, ask for one task ID.
3. Run automation script once per task.
4. Return output path + prompt used.

## Additional Resources

- For implementation details, see [reference.md](reference.md)
- For prompt templates and examples, see [examples.md](examples.md)
