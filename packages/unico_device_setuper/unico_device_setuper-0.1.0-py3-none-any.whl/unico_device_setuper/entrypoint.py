import asyncio
import sys

import typer

import unico_device_setuper
from unico_device_setuper import datadir, main

APP = typer.Typer(pretty_exceptions_enable=False)


def display_version_and_quit():
    print(unico_device_setuper.__version__)
    sys.exit(0)


def display_data_dir_and_quit():
    print(datadir.get())
    sys.exit(0)


@APP.command()
def entrypoint(version: bool = False, show_data_dir: bool = False, restart_server: bool = False):  # noqa: FBT001, FBT002
    if version:
        display_version_and_quit()

    if show_data_dir:
        display_data_dir_and_quit()

    asyncio.run(main.main(main.Args(restart_server=restart_server)))
