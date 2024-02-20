"""Module with functions to transform text."""

from openai import OpenAI

from llmask.model import query_llm

TRANSFORMATION_MAPPING = {
    "s": "simplify",
    "t": "thesaurus",
    "i": "imitate",
}


# OPTIONAL: make functions retun system prompts only, and move queries LLM in model.py?
def thesaurus(
    input: str,
    model_name: str,
    api_client: OpenAI,
) -> str:
    """Change input by replacing words with their synonyms.

    Args:
        input: Text input to be transformed.
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
    model_name: str,
    api_client: OpenAI,
) -> str:
    """Simplify language of input.

    Args:
        input: Text input to be transformed.
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


def apply_transformations(
    input: str,
    persona: str,
    transformations: str,
    model_name: str,
    api_client: OpenAI,
) -> str:
    """Subsequently apply a chain of transformations.

    Each transformed output is passed as input to the next transformation.

    Args:
        input: user-provided text input.
        persona: name of persona whose writing style to imitate.
        transformation_funcs: list of transformation functions to be chained.
        model_name: name of model to use (as known to model server).
        api_client: instance of adapter to model API.
    Return:
        text after pipeline's final transformation.
    """
    for transformation in transformations:
        print(
            f"Applying transformation '{TRANSFORMATION_MAPPING.get(transformation)}':\n"
        )
        match transformation:
            case "s":
                output = simplify(
                    input=input,
                    model_name=model_name,
                    api_client=api_client,
                )
            case "t":
                output = thesaurus(
                    input=input,
                    model_name=model_name,
                    api_client=api_client,
                )
            case "i":
                output = imitate(
                    input=input,
                    persona=persona,
                    model_name=model_name,
                    api_client=api_client,
                )
            case _:
                print(f"Invalid transformation '{transformation}' ! Exiting.")
                exit(1)
        print(f"> {output}\n\n")

        input = output  # use this transformtion's output as next input
    return output
