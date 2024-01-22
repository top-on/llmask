"""Functions for serving/hosting language model locally."""

import os
from pathlib import Path

from llmask.model import Model


def serve_model(model: Model, models_dir: Path) -> None:
    """Run local model server in non-detached mode.

    The llamafile server this is used here exposes an OpenAI-compatible API."""
    # validate input
    model_filepath = models_dir / model.filename
    assert model_filepath.exists(), "Model file not found."

    # make llamafile executable
    result = os.system(f"chmod u+x {model_filepath}")
    assert result == 0, "Could not make model's llamafile executable."

    # serve model (non-detached)
    os.system(f"sh {model_filepath} --nobrowser")
