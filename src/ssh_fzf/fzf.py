import subprocess

"""
# Sample
dir_path = '/home/worker/Downloads/aruba_edge'
cmd1 = ['fzf' , '--multi', '--print0']
# cmd2 = ['fd', '.']
cmd2 = ['cat', dir_path + '/arubaedge_ls.txt']
result = subprocess.run(
    cmd1,
    input=subprocess.check_output(cmd2, cwd=dir_path),
    stdout=subprocess.PIPE,
    shell=True
)
selected = result.stdout.strip().decode() if result.stdout else ''
print(selected)
"""

def select_line_in_dirpath(dir_path):
    cmd1 = ['fzf' , '--multi', '--print0']
    cmd2 = ['ls', dir_path]
    result = subprocess.run(
        cmd1,
        input=subprocess.check_output(cmd2, cwd=dir_path),
        stdout=subprocess.PIPE,
        shell=True
    )
    selected = result.stdout.strip().decode() if result.stdout else ''
    return selected

def select_line_in_file(dir_path, filename):
    cmd1 = ['fzf' , '--multi', '--print0']
    cmd2 = ['cat', f'{dir_path}/{filename}']
    result = subprocess.run(
        cmd1,
        input=subprocess.check_output(cmd2, cwd=dir_path),
        stdout=subprocess.PIPE,
        shell=True
    )
    selected = result.stdout.strip().decode() if result.stdout else ''
    return selected

