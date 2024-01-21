"""Wrapper for prompting LLM."""

# %%
from openai import OpenAI


def get_api_client() -> OpenAI:
    """Get API client to locally running LLM, which has OpenAI compatibility."""
    return OpenAI(
        base_url="http://localhost:8080/v1",
        api_key="sk-no-key-required",
    )


def query_llm(
    api_client: OpenAI,
    instructions: str,
    input: str,
    temperature: float,
    seed: int,
) -> str:
    """Interface function to query LLM and retrieve response.

    Args:
        api_client: Connection to LLM server
        instructions: instructions on how to change input text
        input: input text to be changed
        temperature: parameter passed to LLM
        seed: random seed (for reproducibility)
    Returns:
        response from LLM
    """

    completion = api_client.chat.completions.create(
        model="LLaMA_CPP",
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
