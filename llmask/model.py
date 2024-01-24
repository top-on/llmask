"""Module for model handling."""

from pathlib import Path
from typing import NamedTuple
from urllib.parse import urlparse

import requests
from tqdm import tqdm


class Artifact(NamedTuple):
    name: str
    url: str

    def __str__(self) -> str:
        return self.name

    @property
    def filename(self) -> str:
        return Path(urlparse(self.url).path).name


class Model(Artifact):
    """Definition of a Large Language Model."""


class ModelServer(Artifact):
    """Definition of a Model Server."""


def download_artifact(
    artifact: Artifact,
    cache_dir: Path,
) -> None:
    """Download file with progress bar.

    Creates destination path's parent folder, if it does not exist.

    Args:
        source_url: URL of file to be downloaded.
        dest_path: filepath to save model to.
    """
    # create cache dir, if not exists
    cache_dir.parent.mkdir(parents=True, exist_ok=True)
    # download with progress bar
    artifact_path = cache_dir / artifact.filename
    resp = requests.get(url=artifact.url, stream=True)
    total = int(resp.headers.get("content-length", 0))
    with open(artifact_path, "wb") as file, tqdm(
        desc=str(artifact_path),
        total=total,
        unit="iB",
        unit_scale=True,
        unit_divisor=1024,
    ) as bar:
        for data in resp.iter_content(chunk_size=1024):
            size = file.write(data)
            bar.update(size)
