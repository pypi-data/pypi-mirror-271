import base64
import contextlib
import dataclasses
import sqlite3

from unico_device_setuper import adb, datadir


@dataclasses.dataclass
class Context:
    connection: sqlite3.Connection

    @contextlib.asynccontextmanager
    @staticmethod
    async def make(adb_ctx: adb.Context):
        uninav = adb_ctx.config.uninav
        db_dump_b64 = await adb_ctx.uninav_shell(
            f'base64 /data/data/{uninav.package_name}/databases/{uninav.local_db_name}'
        )
        with datadir.get_temporary() as tmp_dir:
            db_path = tmp_dir / 'dump.db'
            db_path.write_bytes(base64.b64decode(db_dump_b64))
            connection = sqlite3.connect(db_path)
            try:
                yield Context(connection)
            finally:
                connection.close()

    def fetch_all(self, request: str):
        return self.connection.cursor().execute(request).fetchall()
