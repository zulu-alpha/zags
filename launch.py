import os
import sys
import json
from subprocess import run
from urllib.parse import urlparse, parse_qs
import requests


def get_mods


def launch(executable_path, mods_path, mods_manifest_url, mod_line, arguments, kw_arguments):

    run_params = [executable_path]
    for param in arguments:
        run_params.append(f'-{param}')
    for key, value in kw_arguments.items():
        run_params.append(f'-{key}={value}')

    r = requests.get(mods_manifest_url)
    mods_manifest = json.loads(r.text)

    mod_ids = []
    for name in mods_manifest['mod-lines'][mod_line]:
        url = mods_manifest['mods'][name]
        mod_ids.append(parse_qs(urlparse(url).query)['id'][0])

    print(f'Using mod line {mod_line}: {mods_manifest["mod-lines"][mod_line]}')

    mod_param = '-mod='
    for mod_id in mod_ids:
        mod_param += (mods_path + mod_id) + ';'

    run_params.append(mod_param)

    print(f'Launching with params {run_params}')

    run(run_params)

if __name__ == '__main__':
    launch(
        executable_path='/arma3/arma3server',
        mods_path='/mods/steamapps/workshop/content/107410/',
        mods_manifest_url='https://raw.githubusercontent.com/zulu-alpha/mod-lines/master/mods_manifest.json',
        mod_line='recce',
        arguments=('filePatching',),
        kw_arguments={
            'port': '2302',
            'name': 'server',
            'config': '/arma3/server.cfg'
        }
    )
