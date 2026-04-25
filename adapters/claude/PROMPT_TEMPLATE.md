# Claude Prompt Template (for this repository)

Use this template in Claude-like IDE workflows:

```text
You are operating the Low-Level Vision Pixel-to-Pixel engine in this repository.

Given:
- input image path: {input_image}
- task: {task_name}

Steps:
1) Normalize task name to canonical task ID from `.cursor/skills/low-level-vision-p2p/SKILL.md`.
2) Run:
   python .cursor/skills/low-level-vision-p2p/scripts/run_task.py --input "{input_image}" --task "{task_id}" --provider "{provider}" --model "{model}"
3) Return output image path and metadata JSON path.
4) If task is ambiguous, ask one clarification question before execution.
```
