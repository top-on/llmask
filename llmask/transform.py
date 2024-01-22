"""Module with functions to transform text."""

from typing import Callable
from llmask.prompt import get_api_client, query_llm


def thesaurus(input: str) -> str:
    """Change input by replacing words with synonyms."""
    api_client = get_api_client()
    instructions: str = """
        change the user input by replacing each word with their synonyms.
        replace every word. change all words.
        find a word with similar meaning and use it in the original word's place.

        think like a thesaurus, replacing each word.
        but do not change the meaning of the paragraph.
        Only output the changed input.
        Do not start with 'understood' etc.
    """
    response = query_llm(
        api_client=api_client,
        instructions=instructions,
        input=input,
        temperature=1.5,
        seed=42,
    )
    return response


def simplify(input: str) -> str:
    """Simplify language of input."""
    api_client = get_api_client()

    instructions: str = """
        change the user input by simplifying the language.
        replace uncommon words by common ones.
        make the writing as simple as possible.
        make sure that even children would know each word.

        Do not change the input's meaning.
        do not leave out aspects.
        it's important that the output means the same as the input.

        Only output the changed input.
        Do not start with 'understood' etc.
    """
    response = query_llm(
        api_client=api_client,
        instructions=instructions,
        input=input,
        temperature=0.3,
        seed=42,
    )

    return response


TRANSFORMATION_MAPPING = {
    "s": simplify,
    "t": thesaurus,
}


def parse_transformations_string(transformations: str) -> list[Callable]:
    """Parse CLI parameter 'transformations' to list of to-be-applied functions."""
    # check input validity
    for transformation in transformations:
        try:
            assert transformation in TRANSFORMATION_MAPPING.keys()
        except AssertionError:
            print(
                f"Transformation key '{transformation}' is not valid! "
                f"Valid options are: {list(TRANSFORMATION_MAPPING.keys())}. "
                "Exiting."
            )
            exit(1)

    return [TRANSFORMATION_MAPPING[char] for char in transformations]


def chain_apply_transformations(
    input: str,
    transformation_funcs: list[Callable],
) -> list[str]:
    """Apply chain of transformations, passing each result as input to the next step.

    Args:
        input: user-provided text input.
        transformation_funcs: list of transformation functions to be chained.
    Return:
        list of transformed text, for each step of transformation pipeline.
    """
    transformed_texts: list[str] = []  # list with each result of transformation chain
    for transformation_func in transformation_funcs:
        output = transformation_func(input=input)
        transformed_texts.append(output)
        input = output  # use this transformtion's output as next input
    return transformed_texts
