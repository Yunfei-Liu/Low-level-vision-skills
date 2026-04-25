---
name: llv-p2p-claude-adapter
description: Adapter instructions for Claude-like IDE workflows to run low-level vision/pixel-to-pixel image transforms by calling the shared CLI scripts in this repository. Use when the user asks for denoise/deblur/dehaze/depth/edge/mask-style transforms from one input image and wants Claude or non-Cursor IDE usage.
---

# Claude Adapter for LLV-P2P

## Purpose

Provide a Claude-friendly workflow that reuses the same core engine as Cursor:
- input image path
- canonical task ID
- CLI execution

## Canonical command

```bash
python .cursor/skills/low-level-vision-p2p/scripts/run_task.py \
  --input "{input_image}" \
  --task "{task_id}" \
  --provider "{provider}" \
  --model "{model}"
```

Optional:
- `--base-url "{base_url}"`
- `--api-key "{api_key}"`
- `--size "{size}"`

## Agent behavior contract

1. Map user task phrase to canonical task ID.
2. If ambiguous, ask for one task ID only.
3. Execute the command above.
4. Return:
   - output image path
   - metadata JSON path
   - task ID and model used

## Task ID source of truth

Use canonical IDs from:
- `.cursor/skills/low-level-vision-p2p/SKILL.md`

## Prompt template

Use:
- `adapters/claude/PROMPT_TEMPLATE.md`
