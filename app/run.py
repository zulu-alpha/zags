import os
import sys
import json
from subprocess import run
from pathlib import Path
from configuration import render_server_cfg, render_basic_cfg, render_armaprofile


PATH_MODS = '/arma3/mods'
PATH_KEYS = '/arma3/keys'
PATH_MISSIONS = '/arma3/mpmissions'
PATH_MODLINES = str(Path(PATH_MODS) / 'modlines.json')
PATH_SERVER_CFG = '/arma3/server.cfg'
PATH_BASIC_CFG = '/arma3/basic.cfg'
PATH_PROFILE = '/arma3/server/server.armaprofile'

def launch(executable_path, mods_path, mod_line, arguments, kw_arguments):
    """Run the Arma3 Server executable"""
    run_params = [executable_path]
    for param in arguments:
        run_params.append(f'-{param}')
    for key, value in kw_arguments.items():
        run_params.append(f'-{key}={value}')
    with open(PATH_MODLINES, 'r') as open_file:
        modlines = json.loads(open_file.read())
    print(f'Using mod line {mod_line}: {modlines[mod_line]}')
    for mod_dir in modlines[mod_line]:
        run_params.append(f'-mod={str(Path(mods_path) / mod_dir)}')
    print(f'Launching with params {run_params}')
    run(run_params)

if __name__ == '__main__':
    render_server_cfg(PATH_SERVER_CFG)
    render_basic_cfg(PATH_BASIC_CFG)
    render_armaprofile(PATH_PROFILE)
    launch(
        executable_path='/arma3/arma3server',
        mods_path='mods',
        mod_line=os.environ['MODLINE'],
        arguments=('filePatching',),
        kw_arguments={
            'port': '2302',
            'name': 'server',
            'config': PATH_SERVER_CFG,
            'cfg': PATH_BASIC_CFG
        }
    )
