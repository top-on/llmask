"""Main entrypoint."""

import logging
import os
from typing import Callable

from typer import Option, Typer

from llmask.config import CACHE_DIR, MODEL_SERVER, MODELS
from llmask.model import Model, download_artifact
from llmask.serve import serve_model
from llmask.transform import (
    chain_apply_transformations,
    parse_transformations_string,
)

logging.basicConfig(level=logging.WARN)
os.environ["NO_COLOR"] = "1"  # deactivate color for rich/colorama (if installed)

app = Typer(
    name="adverserial_stylometry_llm",
    add_completion=False,
    context_settings={"help_option_names": ["-h", "--help"]},
)


@app.command()
def clear():
    """Delete downloaded files."""
    choice = input("Delete all cached files? [y/N]:")
    if choice != "y":
        print("Cache will not be deleted. Exiting.")
        exit(1)

    cached_files = list(CACHE_DIR.glob("*"))
    print(f"{len(cached_files)} locally cached files to be deleted.")
    for file in cached_files:
        print(f"Removing '{file.name}' from cache ...")
        file.unlink()
    print("Cache cleared.")


# TODO: download choice dialog
@app.command()
def download():
    """Download model server and Large Language Model and into local cache."""
    # OPTIONAL: download model server on demand
    # download model server
    model_server_path = CACHE_DIR / MODEL_SERVER.filename
    if model_server_path.exists():
        print("\n✅ Model server was already downloaded.")
    else:
        print("\n⏳ `Downloading model server ...")
        download_artifact(
            artifact=MODEL_SERVER,
            cache_dir=CACHE_DIR,
        )
        print("Download of model server finished.")

    # lookup downloaded models
    cached_files = {file.name for file in CACHE_DIR.glob("*")}
    cached_models = [model for model in MODELS if model.filename in cached_files]
    if len(cached_models) > 0:
        print("\n📋 The following models were already downloaded:")
        for i, cached_model in enumerate(cached_models):
            print(f" ✅ {cached_model}")
    else:
        print("\nNo models have been downloaded yet.")

    # present download options
    downloadable_models = [model for model in MODELS if model not in cached_models]
    if len(downloadable_models) == 0:
        print(
            "❗️ No further models available for download. Continue with 'llmask serve'."
        )
    print("\n📋 The following models can be downloaded:")
    for i, downloadable_model in enumerate(downloadable_models):
        print(f"\n [{i}]: {downloadable_model}")
    choice = input(
        "\nChoose which model to download "
        f"(from {list(range(len(downloadable_models)))}): "
    )

    # validate and parse choice
    if choice not in [str(index) for index in range(len(downloadable_models))]:
        print(f"❗️ choice must be from list {list(range(len(downloadable_models)))}.")
        exit(1)
    model = downloadable_models[int(choice)]

    # download model
    print("Downloading model...")
    download_artifact(
        artifact=model,
        cache_dir=CACHE_DIR,
    )
    print("Download of model finished. Continue with 'llmask serve'.")


@app.command()
def serve() -> None:
    """Start model server locally.

    The local model server keeps running while Terminal window remains open.
    """
    # check if model server in cache
    if not (CACHE_DIR / MODEL_SERVER.filename).exists():
        print("❗️ Model server not found in local cache. Run 'llmask download' first.")
        exit(1)

    # lookup which models can be chosen
    cached_files = {file.name for file in CACHE_DIR.glob("*")}
    cached_models = [model.name for model in MODELS if model.filename in cached_files]
    if len(cached_models) == 0:
        print("❗️ no models cached. Run 'llmask download' first.")
        exit(1)

    # present options
    print("\n📋 The following models have been downloaded:")
    for i, cached_model in enumerate(cached_models):
        print(f"\n [{i}]: {cached_model}")
    choice = input(
        f"\nChoose which model to serve (from {list(range(len(cached_models)))}): "
    )

    # validate and parse choice
    if choice not in [str(index) for index in range(len(cached_models))]:
        print(f"❗️ choice must be from list {list(range(len(cached_models)))}.")
        exit(1)
    model_name = cached_models[int(choice)]
    model: Model = next(model for model in MODELS if model.name == model_name)

    print(f"\n⏳ Serving model '{model.name}'...\n")
    serve_model(model=model, model_server=MODEL_SERVER, cache_dir=CACHE_DIR)
    print("\nModel server stopped. Exiting.")


@app.command()
def transform(
    transformations: str = Option(
        "ts",
        "-t",
        "--transformations",
        help=(
            "Compact representation of operations "
            "(e.g. 'ts' for the steps 'thesaurus -> simplify')"
        ),
    ),
    input: str = Option(
        ...,
        "-i",
        "--input",
        help="Input text that will be transformed.",
    ),
):
    """Transform input text with chained transformations by Large Language Model."""
    print("\nUser-provided input:\n")
    print(f"> {input}\n\n")

    transformation_funcs: list[Callable] = parse_transformations_string(
        transformations=transformations
    )

    transformed_texts = chain_apply_transformations(
        input=input,
        transformation_funcs=transformation_funcs,
    )

    for func, text in zip(transformation_funcs, transformed_texts):
        print(f"Result after applying transformation '{func.__name__}':\n")
        print(f"> {text}\n\n")


if __name__ == "__main__":
    app()
