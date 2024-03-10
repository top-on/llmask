"""Main entrypoint."""

import logging
import os

from typer import Option, Typer

from llmask.model import get_api_client
from llmask.transform import apply_transformations

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
            "(e.g. 'tsi' for the steps 'thesaurus -> simplify -> imitate')"
        ),
    ),
    input: str = Option(
        ...,
        "-i",
        "--input",
        help="Input text that will be transformed.",
    ),
    persona: str = Option(
        "Ernest Hemingway",
        "-p",
        "--persona",
        help="Name of persona whose writing style to imitate.",
    ),
    model_name: str = Option(
        "nous-hermes2:10.7b-solar-q6_K",
        "-m",
        "--model",
        help="Name of model to use (as known to model server).",
    ),
    url: str = Option(
        "http://localhost:11434/v1",
        "-u",
        "--url",
        help="URL of Open AI compatible model API.",
    ),
    verbose: int = Option(
        0,
        "--verbose",
        "-v",
        count=True,
        help="Verbosity level. At default, only the final output is returned.",
    ),
):
    """Transform input text with chained transformations by a Large Language Model."""
    if verbose > 0:
        print("\n> User-provided input:")
        print(f"\n{input}\n\n")

    api_client = get_api_client(url=url)
    apply_transformations(
        input=input,
        persona=persona,
        transformations=transformations,
        model_name=model_name,
        api_client=api_client,
        verbose=verbose,
    )


if __name__ == "__main__":
    app()
