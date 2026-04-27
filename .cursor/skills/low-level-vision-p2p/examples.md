# Examples

## CLI Example

```bash
python .cursor/skills/low-level-vision-p2p/scripts/run_task.py \
  --input demos/input/street_night.jpg \
  --task low_light_enhance \
  --model gpt-image-2 \
  --size 1024x1024
```

## Batch Example

```bash
python .cursor/skills/low-level-vision-p2p/scripts/run_task.py \
  --input demos/input/portrait.jpg \
  --task denoise

python .cursor/skills/low-level-vision-p2p/scripts/run_task.py \
  --input demos/input/portrait.jpg \
  --task deblur

python .cursor/skills/low-level-vision-p2p/scripts/run_task.py \
  --input demos/input/portrait.jpg \
  --task albedo_layer

python .cursor/skills/low-level-vision-p2p/scripts/run_task.py \
  --input demos/input/portrait.jpg \
  --task shading_layer
```

## Prompt Snapshot Example (`dehaze`)

```text
You are performing a low-level vision pixel-to-pixel transformation.
Task: dehaze

Input image is the only source of truth. Keep scene geometry, camera viewpoint, object identity, and composition unchanged unless task explicitly requires map rendering.

Primary objective:
Reduce atmospheric haze/fog and restore contrast with realistic color and depth cues.

Hard constraints:
- No added or removed objects.
- No text, watermark, logo, or border.
- Keep global framing and perspective consistent with input.
- Preserve fine structures (hair, wires, edges, micro-texture) whenever compatible with the task.

Output specification:
Single realistic RGB image, faithful to source content.

Quality bar:
Natural color, stable local contrast, no over-saturation, no halo artifacts.

If uncertain, prefer conservative edits over aggressive hallucination.
```

## Typical Output Paths

- `outputs/denoise/portrait__denoise.png`
- `outputs/deblur/portrait__deblur.png`
- `outputs/depth_map/street__depth_map.png`
- `outputs/albedo_layer/portrait__albedo_layer.png`
- `outputs/shading_layer/portrait__shading_layer.png`
- `outputs/edge_map/car__edge_map.png`
