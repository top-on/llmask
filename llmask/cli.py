"""Main entrypoint."""

import logging
import os
from typing import Callable

from typer import Typer, Option
from llmask.model import MODEL, MODELS_DIR, download_file
from llmask.serve import serve_model

from llmask.transform import (
    chain_apply_transformations,
    parse_transformations_string,
)

logging.basicConfig(level=logging.WARN)

app = Typer(
    name="adverserial_stylometry_llm",
    add_completion=False,
    context_settings={"help_option_names": ["-h", "--help"]},
)

# deactivate color for rich/colorama (if installed)
os.environ["NO_COLOR"] = "1"


@app.command()
def clear():
    """Delete downloaded files."""
    print("Clearing cached model files...")
    model_path = MODELS_DIR / MODEL.filename
    model_path.unlink(missing_ok=True)
    print("Done.")


@app.command()
def download():
    """Download Large Language Model into local cache."""
    model_path = MODELS_DIR / MODEL.filename
    if model_path.exists():
        print("Model already downloaded. Run 'clear' to make re-download possible.")
    else:
        print("Downloading model...")
        model_path.parent.mkdir(parents=True, exist_ok=True)
        download_file(
            source_url=MODEL.url,
            dest_path=model_path,
        )
        print("Download finished. Continue with 'serve' command.")


@app.command()
def serve() -> None:
    """Start model server locally.

    The local model server keeps running while Terminal window remains open.
    """
    if not (MODELS_DIR / MODEL.filename).exists():
        print("Model not found in local cache. Run 'download' command first. Exiting.")
        exit(1)

    print("Serving model ...")
    serve_model(model=MODEL, models_dir=MODELS_DIR)
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
    print(f"> {input}\n")

    transformation_funcs: list[Callable] = parse_transformations_string(
        transformations=transformations
    )

    transformed_texts = chain_apply_transformations(
        input=input,
        transformation_funcs=transformation_funcs,
    )

    for func, text in zip(transformation_funcs, transformed_texts):
        print(f"Result after applying transformation '{func.__name__}':\n")
        print(f"> {text}\n")


if __name__ == "__main__":
    app()
