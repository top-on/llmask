"""Main entrypoint."""

import logging
import os
import sys

import typer
from typer import Option, Typer

from llmask.model import get_api_client
from llmask.transform import apply_transformations

DEFAULT_MODEL_NAME: str = "nous-hermes2:10.7b-solar-q6_K"
DEFAULT_URL: str = "http://localhost:11434/v1"
DEFAULT_TEMPERATURE: float = 0.5
DEFAULT_SEED: int = 42


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
            "Sequence of transformations to apply in order, "
            "e.g. 'tsp' for the steps 'thesaurus -> simplify -> persona', "
            "where 't' applies thesaurus, 's' simplifies, and 'p' imitates a persona."
        ),
    ),
    input_text: str = Option(
        None,
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
        DEFAULT_MODEL_NAME,
        "-m",
        "--model",
        help="Name of model to use (as known to model server).",
    ),
    url: str = Option(
        DEFAULT_URL,
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
    temperature: float = Option(
        DEFAULT_TEMPERATURE,
        "-r",
        "--randomness",
        help=(
            "Higher values make the output more random."
            "Parameter value is passes as 'sampling temperature' to language model. "
        ),
        min=0.0,
        max=2.0,
    ),
    seed: int = Option(
        DEFAULT_SEED,
        "-s",
        "--seed",
        help=(
            "Repeated requests with the same `seed` and parameters "
            "should return the same result."
        ),
    ),
):
    """Transform input text with chained transformations by a Large Language Model."""
    if verbose > 0:
        print("\n> User-provided input:")
        print(f"\n{input_text}\n\n")

    # if no input parameter set, try to read from stdin/pipe
    if input_text is None:
        if not sys.stdin.isatty():  # check if stdin is connected to a pipe
            input_text = sys.stdin.read()
        else:
            typer.echo(
                message="Need to either provide input (-i) or provide text via stdin!",
                err=True,
            )
            raise typer.Exit(code=1)

    api_client = get_api_client(url=url)
    apply_transformations(
        input_text=input_text,
        persona=persona,
        transformations=transformations,
        model_name=model_name,
        api_client=api_client,
        verbose=verbose,
        temperature=temperature,
        seed=seed,
    )


if __name__ == "__main__":
    app()
