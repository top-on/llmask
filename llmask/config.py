"""Central module for static configuration."""

from pathlib import Path

from llmask.model import Model

MODEL = Model(
    name="mistral-7b-instruct-v0.2.Q3_K_M",
    url="https://huggingface.co/jartine/Mistral-7B-Instruct-v0.2-llamafile/resolve/main/mistral-7b-instruct-v0.2.Q3_K_M.llamafile",
)
MODELS_DIR: Path = Path.home() / ".cache/llmask/models/"

# release location of model server
LLAMAFILE_SERVER_URL: str = (
    "https://github.com/Mozilla-Ocho/llamafile/releases/download/0.6.1/llamafile-0.6.1"
)
