import json
from subprocess import call
from urllib.parse import urlparse, parse_qs
import click
import requests


@click.command()
@click.option('--steamcmd_path', prompt='Path to steamcmd script')
@click.option('--manifest_url', prompt='URL to raw manifest file')
@click.option('--mod_line', prompt='Mod line to update')
@click.option('--path', prompt='Path to steam directory to use', help='Path to steam directory to download to')
@click.option('--username', prompt='Steam Username')
@click.option('--password', prompt='Steam Password')
def update_mods(steamcmd_path, manifest_url, mod_line, path, username, password):
    """Updates mods according to the given mod line decalred in a mods_manifest.json file"""

    r = requests.get(manifest_url)
    mods_manifest = json.loads(r.text)

    click.echo(f"Updating the following mods: {mods_manifest['mod-lines'][mod_line]}")

    mod_ids = []
    for name in mods_manifest['mod-lines'][mod_line]:
        url = mods_manifest['mods'][name]
        mod_ids.append(parse_qs(urlparse(url).query)['id'][0])

    for mod_id in mod_ids:
        call(f'{steamcmd_path} +login {username} {password} +force_install_dir {path} +workshop_download_item "107410" "{mod_id}"')

if __name__ == '__main__':
    update_mods()
