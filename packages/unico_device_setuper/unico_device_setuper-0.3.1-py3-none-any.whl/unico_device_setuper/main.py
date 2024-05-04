import dataclasses

from unico_device_setuper import adb, cfg, local_db


@dataclasses.dataclass
class Args:
    restart_server: bool


async def main(args: Args):
    config = cfg.Config.load()
    async with (
        adb.Context.make(config, restart=args.restart_server) as adb_ctx,
        local_db.Context.make(adb_ctx) as db_ctx,
    ):
        print('metadata', db_ctx.fetch_all('SELECT * FROM android_metadata'))
