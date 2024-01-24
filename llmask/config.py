"""Central module for static configuration."""

from pathlib import Path

from llmask.model import Model, ModelServer

MODELS: list[Model] = [
    Model(
        name="mistral-7b-instruct-v0.2.Q3_K_M",
        url="https://huggingface.co/jartine/Mistral-7B-Instruct-v0.2-llamafile/resolve/main/mistral-7b-instruct-v0.2.Q3_K_M.llamafile",
    ),
    Model(
        name="nous-hermes-llama2-13b.Q4_0",
        url="https://gpt4all.io/models/gguf/nous-hermes-llama2-13b.Q4_0.gguf",
    ),
]

MODEL_SERVER = ModelServer(
    name="llamafile-0.6.1",
    url="https://github.com/Mozilla-Ocho/llamafile/releases/download/0.6.1/llamafile-0.6.1",
)

CACHE_DIR: Path = Path.home() / ".cache/llmask/models/"
