"""Module for model handling."""

from pathlib import Path
from typing import NamedTuple
from urllib.parse import urlparse

import requests
from tqdm import tqdm


def filename_from_url(url: str) -> str:
    """Extract filename from an URL."""
    return Path(urlparse(url).path).name


class Model(NamedTuple):
    """Reference to a Large Language Model."""

    name: str
    url: str

    def __str__(self) -> str:
        return self.name

    @property
    def filename(self) -> str:
        return filename_from_url(url=self.url)


def download_file(
    source_url: str,
    dest_path: Path,
) -> None:
    """Download file with progress bar.

    Creates destination path's parent folder, if it does not exist.

    Args:
        source_url: URL of file to be downloaded.
        dest_path: filepath to save model to.
    """
    # create parent folder
    dest_path.parent.mkdir(parents=True, exist_ok=True)
    # download with progress bar
    resp = requests.get(source_url, stream=True)
    total = int(resp.headers.get("content-length", 0))
    with open(dest_path, "wb") as file, tqdm(
        desc=str(dest_path),
        total=total,
        unit="iB",
        unit_scale=True,
        unit_divisor=1024,
    ) as bar:
        for data in resp.iter_content(chunk_size=1024):
            size = file.write(data)
            bar.update(size)
