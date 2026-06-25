## ssh-fzf
easy ssh manager without remembering host password

## Preparation
### Install sshpass
- Ubuntu
```
sudo apt update && sudo apt install sshpass
```
- RedHat
```
sudo dnf install sshpass
```
### install python packages
- uv
```
uv venv
uv sync
```

## Usage
### Prepare Server
- config/server_config.toml

| key | note |
| - | - |
| masterpassword | masterpassword is needed to auth /api/key | 
| target | hostname list key |
| hostname | receive key to respond password |
| password | password of hostname |


```toml
masterpassword = 'password'

[[target]]
hostname = 'myhost'
password = 'password'

[[target]]
hostname = 'myhost2'
password = 'password2'
```

### Run Server
```
./serv.sh
```
or
```
docker compose -f docker/docker-compose.yml up
```

### Prepare Client
- config/config.toml

| key | note |
| - | - |
| target | hostname list key |
| hostname | target hostname |
| ip | ip to use ssh connection |
| username  | username to use ssh connection |


```toml
[[target]]
hostname = 'myhost'
ip = '192.168.0.1'
username = 'user1'

[[target]]
hostname = 'myhost2'
ip = '192.168.0.2'
username = 'user2'
```

### Run Client
```
./run.sh
```

- select hostname by fzf
- input masterpassword
- ssh session will start
