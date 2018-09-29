import sys
import json
from subprocess import run
from urllib.parse import urlparse, parse_qs
import requests
import jinja2


def launch(manifest_url, mod_line):

    r = requests.get(manifest_url)
    mods_manifest = json.loads(r.text)


    mod_ids = []
    for name in mods_manifest['mod-lines'][mod_line]:
        url = mods_manifest['mods'][name]
        mod_ids.append(parse_qs(urlparse(url).query)['id'][0])

    mod_param = '-mod='
    mod_root_path = '/home/adam/Steam/steamapps/workshop/content/107410/'
    for mod_id in mod_ids:
        mod_param += (mod_root_path + mod_id) + ';'

    print(sys.argv[1:])
    
    #run(['/home/adam/arma3/arma3server', '-port=2302', '-profiles=/home/adam/profiles', '-name=server', '-filePatching', '-config=server.cfg',  mod_param])

if __name__ == '__main__':
    launch('https://raw.githubusercontent.com/zulu-alpha/mod-lines/master/mods_manifest.json', 'main')
