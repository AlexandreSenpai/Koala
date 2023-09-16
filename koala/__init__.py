from sys import version_info as __version
from koala.infra.entrypoints.cli.typer import create_cli

__version__ = '0.0.1'
__author__ = 'AlexandreSenpai'
__email__ = 'alexandreramos469@gmail.com'
__all__ = ['create_cli']

if __version.minor != 3 and __version.minor < 8:
    raise Exception('You must run this application at least on Python 3.8')

