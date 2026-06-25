import os
import getpass
import requests
from mini import misc
from ssh_fzf import load_config

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

def set_sshpass(hostname):
    masterpassword = getpass.getpass('masterpassword: ')
    r = requests.post("http://127.0.0.1:8000/api/key", json={"masterpassword": masterpassword, "hostname": hostname})
    ssh_password = r.json()["value"]
    # ssh_password = getpass.getpass('set SSHPASS: ')
    os.environ['SSHPASS'] = ssh_password

def run_ssh_fzf():
    env = load_config.load_env(['config'])
    target = pick_target(env['config']['target'])
    hostname = target["hostname"]
    set_sshpass(hostname)
    ssh_args = f'{target["username"]}@{target["ip"]}'

    # this will not return to python, just bash-ssh process(can use ctrl-c in ssh, etc.)
    os.execvp("sshpass", ["sshpass", "-e", "ssh", ssh_args])

if __name__ == '__main__':
    run_ssh_fzf()
