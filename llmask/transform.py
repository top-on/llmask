"""Module with functions to transform text."""

from typing import Callable

from openai import OpenAI

from llmask.model import query_llm


# OPTIONAL: make functions retun system prompts only, and move queries LLM in model.py?
def thesaurus(
    input: str,
    persona: str,  # not used, just for interface compatibility
    model_name: str,
    api_client: OpenAI,
) -> str:
    """Change input by replacing words with their synonyms.

    Args:
        input: Text input to be transformed.
        persona: this parameter is not used. It's only for interface compatibility.
        model_name: name of model to use (as known to model server).
        api_client: instance of adapter to model API.
    Return:
        Transformed text.
    """
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
        model_name=model_name,
        temperature=1.5,
        seed=42,
    )
    return response


def simplify(
    input: str,
    persona: str,  # not used, just for interface compatibility
    model_name: str,
    api_client: OpenAI,
) -> str:
    """Simplify language of input.

    Args:
        input: Text input to be transformed.
        persona: this parameter is not used. It's only for interface compatibility.
        model_name: name of model to use (as known to model server).
        api_client: instance of adapter to model API.
    Return:
        Transformed text.
    """
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
        model_name=model_name,
        input=input,
        temperature=0.3,
        seed=42,
    )
    return response


def imitate(
    input: str,
    persona: str,
    model_name: str,
    api_client: OpenAI,
) -> str:
    """Imitate the writing style of a given persona.

    Args:
        input: Text input to be transformed.
        persona: Whose writing style to imitate.
        model_name: name of model to use (as known to model server).
        api_client: instance of adapter to model API.
    Return:
        Transformed text.
    """
    instructions: str = f"""
        change the user input by imitating the writing style of {persona}.
        write in the style of {persona}.
        use the typical words and grammar of {persona}.

        Do not change the input's meaning.
        do not leave out aspects.
        it's important that the output means the same as the input.
        create an output text of similar length as the input.

        Only output the changed input.
        Do not start with 'understood' etc.
    """
    response = query_llm(
        api_client=api_client,
        instructions=instructions,
        model_name=model_name,
        input=input,
        temperature=0.3,
        seed=42,
    )
    return response


TRANSFORMATION_MAPPING = {
    "s": simplify,
    "t": thesaurus,
    "i": imitate,
}


def parse_transformations_string(transformations: str) -> list[Callable]:
    """Parse CLI parameter 'transformations' to list of to-be-applied functions.

    Args:
        transformstions: sequential transformations, in compact string format.
    """
    # check input validity
    if not set(transformations).issubset(TRANSFORMATION_MAPPING.keys()):
        invalid_keys = set(transformations) - set(TRANSFORMATION_MAPPING.keys())
        print(f"Invalid transformation keys: {invalid_keys}! Exiting.")
        exit(1)

    return [TRANSFORMATION_MAPPING[char] for char in transformations]


def chain_apply_transformations(
    input: str,
    persona: str,
    transformation_funcs: list[Callable],
    model_name: str,
    api_client: OpenAI,
) -> list[str]:
    """Apply chain of transformations, passing each result as input to the next step.

    Args:
        input: user-provided text input.
        persona: name of persona whose writing style to imitate.
        transformation_funcs: list of transformation functions to be chained.
        model_name: name of model to use (as known to model server).
        api_client: instance of adapter to model API.
    Return:
        list of transformed text, for each step of transformation pipeline.
    """
    transformed_texts: list[str] = []  # list with each result of transformation chain
    for transformation_func in transformation_funcs:
        output = transformation_func(
            input=input,
            persona=persona,
            model_name=model_name,
            api_client=api_client,
        )
        transformed_texts.append(output)
        input = output  # use this transformtion's output as next input
    return transformed_texts
