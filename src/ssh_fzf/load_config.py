import os
import sys
from mini import misc
from mini.ansi_colors import red

def load_env(key_list):
    error_list = []
    env_values = {}
    for env_key in key_list:
        env = env_key.upper() + '_TOML_PATH'
        value = os.environ.get(env)
        if not value:
            error_list.append(f'{env} is needed')
        env_values[env_key] = misc.read_toml(value)
    if len(error_list) > 0:
        for err in error_list:
            print(red(err))
        sys.exit()
    return env_values

