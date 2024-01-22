"""Functions for serving/hosting language model locally."""

import os

from adversarial_stylometry_llm.model import MODELS_DIR, Model


def serve_model(model: Model) -> None:
    """Run local model server in non-detached mode.

    The llamafile server this is used here exposes an OpenAI-compatible API."""
    # make llamafile executable
    model_path = MODELS_DIR / model.filename
    result = os.system(f"chmod +x {model_path}")
    assert result == 0, "Could not make model's llamafile executable."

    # serve model (non-detached)
    os.system(f"./{model_path} --nobrowser")
