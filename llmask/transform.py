"""Module with functions to transform text."""

from openai import OpenAI

from llmask.model import collect_response_stream, query_llm

TRANSFORMATION_MAPPING = {
    "s": "simplify",
    "t": "thesaurus",
    "p": "persona_imitation",
}


# OPTIONAL: combine transformation functions into a single function
# OPTIONAL: make functions retun system prompts only, and move queries LLM in model.py?
def thesaurus(
    input_text: str,
    model_name: str,
    api_client: OpenAI,
    verbose: int,
    temperature: float,
    seed: int,
) -> str:
    """Change input by replacing words with their synonyms.

    Args:
        input_text: Text input to be transformed.
        model_name: name of model to use (as known to model server).
        api_client: instance of adapter to model API.
        verbose: verbosity level.
        temperature: parameter passed to LLM.
        seed: random seed (for reproducibility).
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
    response_stream = query_llm(
        api_client=api_client,
        instructions=instructions,
        input_text=input_text,
        model_name=model_name,
        temperature=temperature,
        seed=seed,
    )
    response = collect_response_stream(
        response_stream=response_stream,
        print_chunks=verbose > 0,
    )
    return response


def simplify(
    input_text: str,
    model_name: str,
    api_client: OpenAI,
    verbose: int,
    temperature: float,
    seed: int,
) -> str:
    """Simplify language of input.

    Args:
        input_text: Text input to be transformed.
        model_name: name of model to use (as known to model server).
        api_client: instance of adapter to model API.
        verbose: verbosity level.
        temperature: parameter passed to LLM.
        seed: random seed (for reproducibility).
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
    response_stream = query_llm(
        api_client=api_client,
        instructions=instructions,
        model_name=model_name,
        input_text=input_text,
        temperature=temperature,
        seed=seed,
    )
    response = collect_response_stream(
        response_stream=response_stream,
        print_chunks=verbose > 0,
    )
    return response


def persona_imitation(
    input_text: str,
    persona: str,
    model_name: str,
    api_client: OpenAI,
    verbose: int,
    temperature: float,
    seed: int,
) -> str:
    """Imitate the writing style of a given persona.

    Args:
        input_text: Text input to be transformed.
        persona: Whose writing style to imitate.
        model_name: name of model to use (as known to model server).
        api_client: instance of adapter to model API.
        verbose: verbosity level.
        temperature: parameter passed to LLM.
        seed: random seed (for reproducibility).
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
    response_stream = query_llm(
        api_client=api_client,
        instructions=instructions,
        model_name=model_name,
        input_text=input_text,
        temperature=temperature,
        seed=seed,
    )
    response = collect_response_stream(
        response_stream=response_stream,
        print_chunks=verbose > 0,
    )
    return response


def apply_transformations(
    input_text: str,
    persona: str,
    transformations: str,
    model_name: str,
    api_client: OpenAI,
    verbose: int,
    temperature: float,
    seed: int,
) -> str:
    """Subsequently apply a chain of transformations.

    Each transformed output is passed as input to the next transformation.

    Args:
        input_text: user-provided text input.
        persona: name of persona whose writing style to imitate.
        transformation_funcs: list of transformation functions to be chained.
        model_name: name of model to use (as known to model server).
        api_client: instance of adapter to model API.
        verbose: verbosity level.
        temperature: parameter passed to LLM.
        seed: random seed (for reproducibility).
    Return:
        text after pipeline's final transformation.
    """
    for transformation in transformations:
        if verbose > 0:
            print(f"> Applying step '{TRANSFORMATION_MAPPING.get(transformation)}':")
        match transformation:
            case "s":
                output = simplify(
                    input_text=input_text,
                    model_name=model_name,
                    api_client=api_client,
                    verbose=verbose,
                    temperature=temperature,
                    seed=seed,
                )
            case "t":
                output = thesaurus(
                    input_text=input_text,
                    model_name=model_name,
                    api_client=api_client,
                    verbose=verbose,
                    temperature=temperature,
                    seed=seed,
                )
            case "p":
                output = persona_imitation(
                    input_text=input_text,
                    persona=persona,
                    model_name=model_name,
                    api_client=api_client,
                    verbose=verbose,
                    temperature=temperature,
                    seed=seed,
                )
            case _:
                print(f"Invalid transformation '{transformation}' ! Exiting.")
                exit(1)

        input_text = output  # use this transformtion's output as next input

    if verbose == 0:
        print(output)
    return output
