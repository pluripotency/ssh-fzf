import os
import toml
from fastapi import FastAPI

conf_path = os.environ.get('SERVER_CONFIG_TOML_PATH')
with open(conf_path, 'r') as f:
    server_config = toml.loads(f.read())

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello I'm ssh-fzf"}


def find_target(hostname):
    for target in server_config['target']:
        if target['hostname'] == hostname:
            return target['password']

@app.post("/api/key")
def post_key(payload: dict):
    if payload['masterpassword'] == server_config['masterpassword']:
        password = find_target(payload['hostname'])
        return {"value": password}
    return {"value": ""}
