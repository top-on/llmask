"""Wrapper for prompting LLM."""

# %%
from openai import OpenAI


def get_api_client() -> OpenAI:
    """Get API client."""
    return OpenAI(
        base_url="http://localhost:8080/v1",
        api_key="sk-no-key-required",
    )


def query_llm(
    api_client: OpenAI,
    system_prompt: str,
    user_prompt: str,
    **kwargs,
) -> str:
    """Prompt LLM."""

    completion = api_client.chat.completions.create(
        model="LLaMA_CPP",
        # stream=True,  # TODO: test
        messages=[
            {
                "role": "system",
                "content": system_prompt,
            },
            {
                "role": "user",
                "content": user_prompt,
            },
        ],
        **kwargs,
    )

    response = completion.choices[0].message.content
    return response


# %%
api_client = get_api_client()

system_prompt: str = """
"""
user_prompt = """
    In the input paragraph
    * exange as many words as possible with their synonyms.
    * Make sure many words are changed.
    * do not change the meaning too much.

    As output, only return the changed paragraph.
    Do NOT start with 'here is', 'here's' 'sure' or alike.
    Only return the changed paragraph.

    Input paragraph:

    Pakistan on Wednesday recalled its ambassador from Iran.
    And it suspended all Iraninan high-level visits.
    """

response = query_llm(
    api_client=api_client,
    system_prompt=system_prompt,
    user_prompt=user_prompt,
    # max_tokens=50,
    temperature=1.5,
    seed=42,
)
print(response)

# %%
