from sys import version_info
from koala.infra.entrypoints.cli.typer import create_cli


if version_info.minor != 3 and version_info.minor < 8:
    raise Exception('You must run this application at least on Python 3.11')

