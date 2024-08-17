"""Wrapper for prompting LLM."""

# %%
from openai import OpenAI, Stream
from openai.types.chat.chat_completion_chunk import ChatCompletionChunk


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


def query_llm(
    api_client: OpenAI,
    instructions: str,
    input_text: str,
    model_name: str,
    temperature: float,
    seed: int,
) -> Stream[ChatCompletionChunk]:
    """Interface function to query LLM and retrieve response.

    Args:
        api_client: Instance of client for model API
        instructions: instructions on how to change input text
        input_text: input text to be changed
        model_name: name of LLM to be used (known to model server)
        temperature: parameter passed to LLM
        seed: random seed (for reproducibility)
    Returns:
        Response stream from LLM
    """
    response_stream = api_client.chat.completions.create(
        model=model_name,
        messages=[
            {
                "role": "system",
                "content": instructions,
            },
            {
                "role": "user",
                "content": input_text,
            },
        ],
        temperature=temperature,
        seed=seed,
        stream=True,
    )
    return response_stream


def collect_response_stream(
    response_stream: Stream[ChatCompletionChunk],
    print_chunks: bool,
) -> str:
    """Collect response from LLM response stream.

    Args:
        response_stream: stream of LLM response chunks
        print_chunks: whether to print chunks as they come in
    Returns:
        Full response from LLM.
    """
    response: str = ""

    if print_chunks:
        print()
    for chunk in response_stream:
        delta: str = chunk.choices[0].delta.content  # type: ignore
        response += delta
        if print_chunks:
            print(
                delta,
                end="",  # no newline after print
                flush=True,  # print to terminal immediately
            )

    if print_chunks:
        print("\n\n")
    return response


# %%
