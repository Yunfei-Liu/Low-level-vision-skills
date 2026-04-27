# VS Code Adapter

## Quick setup

1. Create `.vscode/` in project root if missing.
2. Copy:
   - `adapters/vscode/tasks.json.example` -> `.vscode/tasks.json`
3. Ensure dependencies and API key are configured.

## Run in VS Code

- Open Command Palette -> `Tasks: Run Task`
- Choose:
  - `LLV-P2P: Run single task`
  - `LLV-P2P: Run batch manifest`

The task will prompt for image path / task ID / provider / model.

## Notes

- Default provider: `openai`
- Supported providers in task picker: `openai`, `openai_compatible`
- For `openai_compatible`, set `OPENAI_BASE_URL` and API key in your environment
