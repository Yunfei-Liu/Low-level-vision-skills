# IDE Integration Guide

This project is designed as:
- **Core engine**: provider-agnostic CLI scripts
- **IDE adapters**: thin wrappers or prompt conventions for each IDE

Core scripts:
- `.cursor/skills/low-level-vision-p2p/scripts/run_task.py`
- `.cursor/skills/low-level-vision-p2p/scripts/run_batch.py`

## Support Matrix

| IDE / Agent | Status | Integration mode |
|---|---|---|
| Cursor | Ready | Native Cursor Skill (`.cursor/skills/...`) |
| Claude-based IDE workflows | Ready (adapter) | Prompt/command adapter that calls the same CLI |
| VS Code | Ready (adapter) | Use task runner template in `adapters/vscode/` |
| Other IDEs (JetBrains, etc.) | Ready | Run CLI directly in terminal/tasks |

## Common One-Command Pattern

```bash
python .cursor/skills/low-level-vision-p2p/scripts/run_task.py \
  --input demos/input/denoise_input.png \
  --task denoise \
  --provider openai \
  --model gpt-image-2
```

## Claude Adapter

See:
- `adapters/claude/SKILL.md`
- `adapters/claude/PROMPT_TEMPLATE.md`

The adapter tells Claude-like agents to:
1. Normalize task name to canonical task ID.
2. Build/validate prompt constraints.
3. Execute the shared CLI command.
4. Return output image path and metadata path.

## VS Code Adapter

See:
- `adapters/vscode/README.md`
- `adapters/vscode/tasks.json.example`

This adapter provides ready-to-use VS Code tasks for:
- single image task execution
- batch manifest execution

## For Other IDEs

Any IDE that can run shell commands can integrate this skill by:
1. Creating a task/command snippet that maps `{input, task}` to CLI arguments.
2. Optionally exposing `--provider`, `--base-url`, and `--model`.
3. Reading output JSON for reproducibility in UI.
