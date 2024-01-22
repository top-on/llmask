"""Module for model handling."""

import requests
from pathlib import Path
from tqdm import tqdm
from urllib.parse import urlparse

from pydantic import BaseModel

MODELS_DIR = Path("models/")


class Model(BaseModel):
    name: str
    url: str

    def __str__(self) -> str:
        return self.name

    @property
    def filename(self) -> str:
        return Path(urlparse(self.url).path).name


MODEL = Model(
    name="mistral-7b-instruct-v0.2.Q3_K_M",
    url="https://huggingface.co/jartine/Mistral-7B-Instruct-v0.2-llamafile/resolve/main/mistral-7b-instruct-v0.2.Q3_K_M.llamafile",
)


def download_file(
    source_url: str,
    dest_path: Path,
) -> None:
    """Download file with progress bar.

    Args:
        source_url: URL of file to be downloaded.
        dest_path: filepath to save model to.
    """
    resp = requests.get(source_url, stream=True)
    total = int(resp.headers.get("content-length", 0))
    # Can also replace 'file' with a io.BytesIO object
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
