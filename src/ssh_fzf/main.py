import os
import sys
import getpass
import requests
from requests.adapters import HTTPAdapter
from mini import misc
from ssh_fzf import load_config

class HostnameIgnoreAdapter(HTTPAdapter):
    def init_poolmanager(self, *args, **kwargs):
        kwargs['assert_hostname'] = False
        return super().init_poolmanager(*args, **kwargs)


def pick_target(target_list):
    from ssh_fzf import fzf
    contents = []
    for node_dict in target_list:
        hostname = node_dict['hostname']
        username = node_dict['username']
        access_ip = node_dict['ip']
        contents.append(f'{hostname}:{username} {access_ip}')
    filename = 'targets'
    dir_path = '/tmp/fzftmp'
    misc.prepare_dir(dir_path)
    file_path = f'{dir_path}/{filename}'
    misc.open_write(file_path, '\n'.join(contents))
    selected = fzf.select_line_in_file(dir_path, filename)
    selected_key = selected.split(' ')[0]
    selected_hostname, selected_username = selected_key.split(':')
    return misc.find(target_list, lambda item: item['hostname'] == selected_hostname and item['username'] == selected_username)

def set_sshpass(hostname, username, server_config):
    masterpassword = getpass.getpass('masterpassword: ')
    server_url = server_config.get('url', 'https://127.0.0.1:8000')
    cert_path = server_config.get('cert_path', 'cert/cert.pem')
    
    # Resolve relative cert_path relative to CONFIG_TOML_PATH directory
    if cert_path and not os.path.isabs(cert_path):
        config_toml_path = os.environ.get('CONFIG_TOML_PATH')
        if config_toml_path:
            config_dir = os.path.dirname(os.path.abspath(config_toml_path))
            cert_path = os.path.normpath(os.path.join(config_dir, cert_path))

    session = requests.Session()
    session.mount('https://', HostnameIgnoreAdapter())
    r = session.post(f"{server_url.rstrip('/')}/api/ssh-fzf", json={"masterpassword": masterpassword, "hostname": hostname, "username": username}, verify=cert_path)
    ssh_password = r.json()["value"]
    os.environ['SSHPASS'] = ssh_password

def run_ssh_fzf():
    env = load_config.load_env(['config'])
    target = pick_target(env['config']['target'])
    hostname = target["hostname"]
    username = target["username"]
    server_config = env['config'].get('server', {})
    set_sshpass(hostname, username, server_config)
    ssh_args = f'{username}@{target["ip"]}'

    print(f'connecting to {ssh_args}')
    sys.stdout.flush()
    sys.stderr.flush()
    os.execvp("sshpass", ["sshpass", "-e", "ssh", "-o", "StrictHostKeyChecking=accept-new", ssh_args])

if __name__ == '__main__':
    run_ssh_fzf()
