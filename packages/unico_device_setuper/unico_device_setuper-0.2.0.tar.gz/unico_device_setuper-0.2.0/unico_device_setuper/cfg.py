import pathlib

import pydantic
import slcfg

from unico_device_setuper import datadir


class Uninav(pydantic.BaseModel):
    package_name: str
    local_db_name: str


class AdbDownloadUrls(pydantic.BaseModel):
    mac_os: pydantic.HttpUrl
    windows: pydantic.HttpUrl
    linux: pydantic.HttpUrl


class Adb(pydantic.BaseModel):
    download_urls: AdbDownloadUrls


class Config(pydantic.BaseModel):
    uninav: Uninav
    adb: Adb

    @staticmethod
    def user_path():
        return datadir.get() / 'config.json'

    def dump(self):
        cfg_path = Config.user_path()
        cfg_path.parent.mkdir(parents=True, exist_ok=True)
        cfg_path.write_text(self.model_dump_json())

    @staticmethod
    def load():
        cfg_path = Config.user_path()
        if not cfg_path.exists():
            default_toml_path = pathlib.Path(__file__).with_suffix('.toml')
            slcfg.read_config(Config, [slcfg.toml_file_layer(default_toml_path)]).dump()
        return slcfg.read_config(Config, [slcfg.json_file_layer(cfg_path)])
