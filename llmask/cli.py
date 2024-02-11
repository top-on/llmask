"""Main entrypoint."""

import logging
import os
from typing import Callable

from typer import Option, Typer

from llmask.transform import (
    chain_apply_transformations,
    parse_transformations_string,
)

logging.basicConfig(level=logging.WARN)
os.environ["NO_COLOR"] = "1"  # deactivate color for rich/colorama (if installed)

app = Typer(
    name="llmask",
    add_completion=False,
    context_settings={"help_option_names": ["-h", "--help"]},
)


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
