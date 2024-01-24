"""Functions for serving/hosting language model locally."""

import os
from pathlib import Path

from llmask.model import Model, ModelServer


def serve_model(
    model: Model,
    model_server: ModelServer,
    cache_dir: Path,
) -> None:
    """Run local model server in non-detached mode.

    The llamafile server this is used here exposes an OpenAI-compatible API.

    Args:
        model: model to serve.
        model_server: server application to serve model with.
        cache_dir: path to local cache folder.
    """
    # check if model and model server exist
    model_path = cache_dir / model.filename
    assert model_path.exists(), "Model file not found. Run 'download'."
    model_server_path = cache_dir / model_server.filename
    assert model_server_path.exists(), "Model server file not found. Run 'download'."

    # make model server executable
    result = os.system(f"chmod u+x {model_server_path}")
    assert result == 0, "Could not make model server executable."

    # serve model (non-detached process)
    os.system(
        command=(
            f"sh {model_server_path} --server "
            "--nobrowser "  # prevent browser pop-up
            "--log-disable "  # do not save answers to disk, for privacy
            f"--model {model_path}"
        )
    )
