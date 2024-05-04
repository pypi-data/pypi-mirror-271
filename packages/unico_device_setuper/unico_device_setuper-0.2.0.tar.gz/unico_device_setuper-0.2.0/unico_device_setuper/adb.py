import contextlib
import dataclasses
import pathlib
import stat
import zipfile

import httpx

from unico_device_setuper import cfg, datadir, dl, helpers


async def get_exe_path(config: cfg.Config):
    data_dir = datadir.get()
    archive_path = data_dir / 'adb.zip'
    if not archive_path.exists():
        async with httpx.AsyncClient() as http_client:
            await dl.download_url(config.adb.download_urls.mac_os, archive_path, http_client)
    adb_dir = data_dir / 'adb'
    if not adb_dir.exists():
        with zipfile.ZipFile(archive_path, 'r') as zip_ref:
            zip_ref.extractall(adb_dir)
    adb_exe = adb_dir / 'platform-tools' / 'adb'
    adb_exe.chmod(adb_exe.stat().st_mode | stat.S_IXUSR)
    return adb_exe


@dataclasses.dataclass
class Context:
    config: cfg.Config
    adb_exe: pathlib.Path

    async def _exec(self, *args: str):
        return await helpers.exec_proc(self.adb_exe, *args)

    @contextlib.asynccontextmanager
    @staticmethod
    async def make(config: cfg.Config, *, restart: bool):
        ctx = Context(config, await get_exe_path(config))
        if restart:
            await ctx._exec('kill-server')
        await ctx._exec('start-server')
        yield ctx

    async def shell(self, cmd: str):
        return await self._exec('shell', cmd)

    async def uninav_shell(self, cmd: str):
        return await self.shell(f'run-as {self.config.uninav.package_name} {cmd}')
