import os
import sys
import json
from subprocess import run
from pathlib import Path


MODLINES_PATH = '/arma3/mods/modlines.json'

def launch(executable_path, mods_path, mod_line, arguments, kw_arguments):
    run_params = [executable_path]
    for param in arguments:
        run_params.append(f'-{param}')
    for key, value in kw_arguments.items():
        run_params.append(f'-{key}={value}')
    with open(MODLINES_PATH, 'r') as open_file:
        modlines = json.loads(open_file.read())
    print(f'Using mod line {mod_line}: {modlines[mod_line]}')
    for mod_dir in modlines[mod_line]:
        run_params.append(f'-mod={str(Path(mods_path) / mod_dir)}')
    print(f'Launching with params {run_params}')
    run(run_params)

if __name__ == '__main__':
    launch(
        executable_path='/arma3/arma3server',
        mods_path='/arma3/mods',
        mod_line='recce',
        arguments=('filePatching',),
        kw_arguments={
            'port': '2302',
            'name': 'server',
            'config': '/arma3/server.cfg'
        }
    )
