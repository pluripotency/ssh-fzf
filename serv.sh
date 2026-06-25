#! /bin/bash
export SERVER_CONFIG_TOML_PATH=./config/server_config.toml

. ./.venv/bin/activate
uv pip install uvicorn fastapi
python server.py

