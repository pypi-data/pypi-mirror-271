import contextlib
import pathlib
import tomllib

import platformdirs

import unico_device_setuper
from unico_device_setuper import helpers


def is_release_version():
    pyproject_path = helpers.module_path(unico_device_setuper).parent / 'pyproject.toml'
    with contextlib.suppress(FileNotFoundError):
        pyproject = tomllib.loads(pyproject_path.read_text())
        if pyproject.get('tool', {}).get('poetry', {}).get('name') == unico_device_setuper.__name__:
            return False
    return True


def get():
    if is_release_version():
        return pathlib.Path(
            platformdirs.user_data_dir(
                appname='com.unico.dev.device_setuper', version=unico_device_setuper.__version__
            )
        ).absolute()

    return helpers.module_path(unico_device_setuper).parent / 'data'


@contextlib.contextmanager
def get_temporary():
    with helpers.temporary_dir(get()) as dir:
        yield dir
