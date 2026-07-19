#! /bin/bash
export SERVER_CONFIG_TOML_PATH=./server_config.toml
export CERT_PATH=../../cert

. ./.venv/bin/activate
uv pip install uvicorn fastapi toml
python server.py

