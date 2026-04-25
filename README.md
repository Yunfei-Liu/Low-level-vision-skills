# Low-Level Vision P2P Skill (GPT-Image)

Language: **English** | [中文](./README.zh-CN.md)

Turn one input image into task-specific low-level vision outputs with a single task name.

This repository provides:
- A production-ready Cursor Skill for image-to-image low-level/pixel-to-pixel transforms
- A standardized task taxonomy and prompt contract
- A runnable automation script powered by frontier image models (`gpt-image-2` by default)
- A demo gallery layout you can quickly fill with your own results
- A batch runner for fast multi-task showcase generation

## Why this is useful

- **Unified interface**: one `--input` + one `--task`
- **Prompt quality control**: consistent hard constraints to reduce hallucination
- **Reproducibility**: output metadata captures full prompt + model + size
- **Publish-friendly**: includes skill files and gallery structure for GitHub showcase

## Supported task families

- Restoration: denoise, deblur, super-resolution, dehaze, derain, low-light enhancement, artifact removal, etc.
- Dense map outputs: edge maps, depth maps, normal maps, saliency, masks, segmentation-like maps
- Geometry-preserving transforms: rectification, structural inpainting, local outpainting
- Domain translation (pixel-aligned preference): photo/sketch, map/satellite-like

Full list lives in:
- `.cursor/skills/low-level-vision-p2p/SKILL.md`

## Quick start

### 1) Install dependencies

```bash
python -m venv .venv
source .venv/bin/activate
pip install openai pillow
```

### 2) Set API key

```bash
export OPENAI_API_KEY="your_key_here"
```

### 3) Run one task

```bash
python .cursor/skills/low-level-vision-p2p/scripts/run_task.py \
  --input demos/input/example.jpg \
  --task dehaze \
  --model gpt-image-2 \
  --size 1024x1024
```

Generated files:
- `outputs/dehaze/example__dehaze.png`
- `outputs/dehaze/example__dehaze.json`

### 4) Run a demo batch

```bash
python .cursor/skills/low-level-vision-p2p/scripts/run_batch.py \
  --manifest demos/tasks.example.json \
  --model gpt-image-2 \
  --size 1024x1024
```

## Demo gallery template

Put your curated before/after pairs in `demos/gallery/` and update this table:

| Task | Input | Output | Notes |
|---|---|---|---|
| `denoise` | `demos/gallery/denoise_input.jpg` | `demos/gallery/denoise_output.png` | texture-preserving |
| `deblur` | `demos/gallery/deblur_input.jpg` | `demos/gallery/deblur_output.png` | anti-halo |
| `low_light_enhance` | `demos/gallery/low_light_input.jpg` | `demos/gallery/low_light_output.png` | shadow visibility |
| `dehaze` | `demos/gallery/dehaze_input.jpg` | `demos/gallery/dehaze_output.png` | natural color |
| `edge_map` | `demos/gallery/edge_input.jpg` | `demos/gallery/edge_output.png` | white-on-black |
| `depth_map` | `demos/gallery/depth_input.jpg` | `demos/gallery/depth_output.png` | near bright, far dark |
| `semantic_segmentation_map` | `demos/gallery/seg_input.jpg` | `demos/gallery/seg_output.png` | coherent regions |

## Skill trigger examples

The skill should activate when user asks things like:
- "把这张图做去噪"
- "use this image to generate a depth map"
- "do pixel-to-pixel dehaze from this input"
- "turn this photo into clean line art"

## Repository structure

```text
.cursor/skills/low-level-vision-p2p/
  SKILL.md
  reference.md
  examples.md
  scripts/run_task.py
demos/
  input/
  gallery/
outputs/
```

## Suggested release checklist

- Add 8-12 representative gallery cases (indoor, outdoor, portrait, night, texture-rich)
- Include one failure-case section (what not to expect)
- Add benchmark notes (subjective quality + latency)
- Pin dependency versions in `requirements.txt` if needed
- Add LICENSE and CITATION if your org requires it

## Roadmap ideas

- Add deterministic post-checkers (SSIM/LPIPS/edge consistency) for regression tracking
- Add task-specific presets (`fast`, `balanced`, `quality`)
- Add automatic markdown gallery generation from `outputs/`
- Add optional multimodel backend adapter (OpenAI, others)
