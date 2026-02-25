# AGENTS.md

## Cursor Cloud specific instructions

### Project overview

InkTime is an AI-powered e-ink digital photo frame project (Python/Flask). See `README.md` for full details.

### Services

| Service | Command | Port | Notes |
|---------|---------|------|-------|
| Flask server | `python3 server.py` | 8765 | Main web server + ESP32 download API |

### Prerequisites for running the server

1. `config.py` must exist (copy from `config-example.py`).
2. A test photo directory (default `./test`) and SQLite DB (`photos.db`) must exist for the WebUI to show data. Without `photos.db`, `/review` returns 404.
3. No external services (databases, caches, etc.) are required — SQLite is file-based.

### How to run

```bash
pip install -r requirements.txt
cp config-example.py config.py   # only if config.py doesn't exist
python3 server.py                # starts Flask on 0.0.0.0:8765
```

### Lint / Test / Build

- This project has **no linter configuration** and **no automated test suite**.
- There is no build step; all Python scripts run directly.
- To verify imports: `python3 -c "import flask, requests, PIL; print('OK')"`

### Gotchas

- `server.py` imports `config` as `cfg` at module level. If `config.py` is missing, the server fails to start with `ModuleNotFoundError`.
- `server.py` also imports `render_daily_photo` at module level, which itself imports `config`. Both must be importable.
- The `IMAGE_DIR` in `config.py` defaults to `./test`. Ensure this directory exists.
- `DOWNLOAD_KEY` in `config.py` must be non-empty or the server raises `SystemExit`.
