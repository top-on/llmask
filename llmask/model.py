"""Wrapper for prompting LLM."""

# %%
from openai import OpenAI


def get_api_client(url: str) -> OpenAI:
    """Get API client to locally running LLM, which has OpenAI compatibility.

    Args:
        url: URL to OpenAI compatible model API.
    Return:
        Instance of client for model API.
    """
    return OpenAI(
        base_url=url,
        api_key="sk-no-key-required",
    )


# OPTIONAL: pass down model name
def query_llm(
    api_client: OpenAI,
    instructions: str,
    input: str,
    model_name: str,
    temperature: float,
    seed: int,
) -> str:
    """Interface function to query LLM and retrieve response.

    Args:
        api_client: Instance of client for model API
        instructions: instructions on how to change input text
        input: input text to be changed
        model_name: name of LLM to be used (known to model server)
        temperature: parameter passed to LLM
        seed: random seed (for reproducibility)
    Returns:
        Response text from LLM
    """
    completion = api_client.chat.completions.create(
        model=model_name,
        messages=[
            {
                "role": "system",
                "content": instructions,
            },
            {
                "role": "user",
                "content": input,
            },
        ],
        temperature=temperature,
        seed=seed,
    )

    response = str(completion.choices[0].message.content)
    return response


# %%
