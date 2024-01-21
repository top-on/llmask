"""Main entrypoint."""

# %%
import logging
import os
from typing import Callable

from typer import Typer, Option

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
def transform(
    transformations: str = Option(
        ...,
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
