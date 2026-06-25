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
        access_ip = node_dict['ip']
        contents.append(f'{hostname} {access_ip}')
    filename = 'targets'
    dir_path = '/tmp/fzftmp'
    misc.prepare_dir(dir_path)
    file_path = f'{dir_path}/{filename}'
    misc.open_write(file_path, '\n'.join(contents))
    selected = fzf.select_line_in_file(dir_path, filename)
    selected_hostname = selected.split(' ')[0]
    return misc.find(target_list, lambda item: item['hostname'] == selected_hostname)

def set_sshpass(hostname, server_config):
    masterpassword = getpass.getpass('masterpassword: ')
    server_url = server_config.get('url', 'https://127.0.0.1:8000')
    cert_path = server_config.get('cert_path', 'cert/cert.pem')
    session = requests.Session()
    session.mount('https://', HostnameIgnoreAdapter())
    r = session.post(f"{server_url.rstrip('/')}/api/key", json={"masterpassword": masterpassword, "hostname": hostname}, verify=cert_path)
    ssh_password = r.json()["value"]
    # ssh_password = getpass.getpass('set SSHPASS: ')
    os.environ['SSHPASS'] = ssh_password

def run_ssh_fzf():
    env = load_config.load_env(['config'])
    target = pick_target(env['config']['target'])
    hostname = target["hostname"]
    server_config = env['config'].get('server', {})
    set_sshpass(hostname, server_config)
    ssh_args = f'{target["username"]}@{target["ip"]}'

    # this will not return to python, just bash-ssh process(can use ctrl-c in ssh, etc.)
    print(f'connecting to {ssh_args}')
    sys.stdout.flush()
    sys.stderr.flush()
    os.execvp("sshpass", ["sshpass", "-e", "ssh", "-o", "StrictHostKeyChecking=accept-new", ssh_args])

if __name__ == '__main__':
    run_ssh_fzf()
