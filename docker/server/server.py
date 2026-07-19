import os
import toml
from fastapi import FastAPI

conf_path = os.environ.get('SERVER_CONFIG_TOML_PATH')
cert_path = os.environ.get('CERT_PATH')
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

if __name__ == "__main__":
    import uvicorn
    host = os.environ.get("HOST", "127.0.0.1")
    uvicorn.run(
        "server:app",
        host=host,
        port=8000,
        ssl_keyfile=f"{cert_path}/key.pem",
        ssl_certfile=f"{cert_path}/cert.pem",
        reload=True
    )

