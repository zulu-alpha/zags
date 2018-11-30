#!/usr/bin/env python3
import os
from subprocess import run


IMAGE_NAME = 'phoenixza/zags'

def docker_build_and_push():
    """Build and push a dockerfile"""
    run(['docker', 'build', '.', '-t', 'phoenixza/zags', '--no-cache',
         '--build-arg', f'STEAM_USERNAME={os.environ["STEAM_USERNAME"]}',
         '--build-arg', f'STEAM_PASSWORD={os.environ["STEAM_PASSWORD"]}'])
    run(['docker', 'login', '-u', os.environ['DOCKER_USERNAME'], '-p', os.environ['DOCKER_PASSWORD']])
    run(['docker', 'push', IMAGE_NAME])

if __name__ == '__main__':
    docker_build_and_push()
