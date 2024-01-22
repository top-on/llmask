"""Main entrypoint."""

# %%
import logging
import os
from typing import Callable

from typer import Typer, Option
from adversarial_stylometry_llm.model import MODEL, MODELS_DIR, download_file

from adversarial_stylometry_llm.transform import (
    parse_transformations_string,
)

logging.basicConfig(level=logging.INFO)

# %%
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
        download_file(
            source_url=MODEL.url,
            dest_path=model_path,
        )
        print("Download finished. Continue with 'transform' command.")


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
    logging.info(f"'transform' called with {transformations=}, {input=}")
    # %%
    transformation_funcs: list[Callable] = parse_transformations_string(
        transformations=transformations
    )

    # TODO: bring to function
    texts: list[str] = [input]  # list with each result of transformation chain
    for transformation_func in transformation_funcs:
        latest_text = texts[-1]
        output = transformation_func(input=latest_text)
        texts.append(output)

    for text in texts:
        print(text)


# %%
if __name__ == "__main__":
    app()