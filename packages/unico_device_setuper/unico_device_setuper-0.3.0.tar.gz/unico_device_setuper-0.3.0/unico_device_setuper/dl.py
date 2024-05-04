import pathlib

import httpx
import pydantic
import tqdm


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
