import asyncio
import contextlib
import pathlib
import shutil
import subprocess
import types
import uuid

import httpx
import pydantic
import tqdm

### Path stuff


def module_path(module: types.ModuleType):
    module_file = module.__file__
    assert module_file is not None
    return pathlib.Path(module_file).parent.absolute()


@contextlib.contextmanager
def temporary_dir(base: pathlib.Path):
    dir = base / str(uuid.uuid4())
    dir.mkdir(exist_ok=True, parents=True)
    try:
        yield dir
    finally:
        shutil.rmtree(dir)


### Subprocess stuff


async def _read_loop(stream: asyncio.StreamReader | None, storage: list[str]):
    if stream is None:
        return
    while True:
        line = await stream.readline()
        if len(line) == 0:
            break
        storage.append(line.decode())


async def exec_proc(exe: pathlib.Path, *args: str):
    process = await asyncio.subprocess.create_subprocess_exec(
        exe, *args, stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )
    stdout_lines: list[str] = []
    stderr_lines: list[str] = []

    stdout_reader = asyncio.get_event_loop().create_task(_read_loop(process.stdout, stdout_lines))
    stderr_reader = asyncio.get_event_loop().create_task(_read_loop(process.stderr, stderr_lines))
    (return_code, _, _) = await asyncio.gather(process.wait(), stdout_reader, stderr_reader)

    stdout = ''.join(stdout_lines)
    stderr = ''.join(stderr_lines)

    if return_code != 0:
        raise RuntimeError(
            f'Command {exe.name} {' '.join(args)} returned {return_code}',
            f'stdout: {stdout}' f'stderr: {stderr}',
        )

    return stdout


### Http stuff


async def download_url(
    url: pydantic.HttpUrl, file_path: pathlib.Path, http_client: httpx.AsyncClient
):
    async with http_client.stream(method='GET', url=str(url)) as resp:
        if resp.status_code != 200:
            content = resp.read().decode('utf-8')
            raise RuntimeError(f'Failed to download {url}: {content} (code {resp.status_code})')
        content_length = int(resp.headers.get('content-length', 0))
        tmp_file_path = file_path.with_stem(file_path.stem + '_tmp')
        tmp_file_path.parent.mkdir(parents=True, exist_ok=True)

        progress_bar = tqdm.tqdm(
            total=content_length,
            desc=(url.path or '').split('/')[-1],
            unit='B',
            unit_scale=True,
            unit_divisor=1024,
        )
        with tmp_file_path.open(mode='wb') as f:
            async for data in resp.aiter_bytes(chunk_size=1024):
                size = f.write(data)
                progress_bar.update(size)
        tmp_file_path.replace(file_path)
