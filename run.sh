#! /bin/bash
export CONFIG_TOML_PATH=./config/config.toml

. ./.venv/bin/activate
uv pip install .
uv run src/ssh_fzf/main.py
