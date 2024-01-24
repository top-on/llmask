# LLMask [ɛl ɛl 'ma:sk]

A command-line tool for masking authorship of text,
by changing the writing style with a Large Language Model.

The main use cases of masking an author's writing sytle are:

* anonymizing a text's author
* protecting the identity of whistleblowers and activists
* see more at [Adversarial Stylometry](https://en.wikipedia.org/wiki/Adversarial_stylometry)

## Disclaimer

⚠️ This project currently is just a demo of what LLMs can do for authorship anonymization.<br>
⚠️ There is no proof that this tool can beat state of the art de-anonymization methods!

### Known Limitations

Despite it's pre-production status, this library has several known limitations:

1. Only a limited number of transformations are implemented (see `transform.py`).
2. Long chains of transformations have observed to make the LLM output artifacts.

## Example workflow

1. choose which Large Language Model to download:

```
$ llmask download


✅ Model server was already downloaded.

📋 The following models were already downloaded:
 ✅ mistral-7b-instruct-v0.2.Q3_K_M

📋 The following models can be downloaded:

 [0]: nous-hermes-llama2-13b.Q4_0

Choose which model to download (from [0]):
```

2. Serve downloaded model on your local machine (keep that terminal open):

```
$ llmask serve


📋 The following models have been downloaded:

 [0]: mistral-7b-instruct-v0.2.Q3_K_M

Choose which model to serve (from [0]):
```

3. Mask your writing style by transforming it into a different one:

```
$ llmask transform -i "this was a triumph. i'm making a note here: huge success."


User-provided input:

> this was a triumph. i'm making a note here: huge success.


Result after applying transformation 'thesaurus':

> This was an astonishing achievement. I'll jot down: extraordinary victory.


Result after applying transformation 'simplify':

> This was a great success. I'll write down: wonderful win.
```

## Getting started
### System requirements

This library is tested on *Apple Silicon*, but it is expected to run on x86, too.

### Installation

This tool can be installed with `poetry install`.

### Usage options

```
$ llmask -h
Usage: llmask [OPTIONS]

  Transform input text with chained transformations by Large Language Model.

Options:
  -t, --transformations TEXT  Compact representation of operations (e.g. 'ts'
                              for the steps 'thesaurus -> simplify')
                              [default: ts]
  -i, --input TEXT            Input text that will be transformed.  [required]
  -h, --help                  Show this message and exit.
```

## Used Large Language Model

This project supports the following LLMs:
* mistral-7b-instruct-v0.2.Q3_K_M
* nous-hermes-llama2-13b.Q4_0

### Other positive evaluations
Some models show promise, and could be integrated into this tool:
* wizardlm-13b-v1.2.Q4_0.gguf -> runs with llamafile server, obeys capitalization less with current prompts

### Other negative evlauations
Some other models have been evaluated negatively, for different reasons:
* mistral-7b-instruct-v0.2.Q5_K_S.llamafile -> gave meaningless/confused responses
* mixtral-8x7b-instruct-v0.1.Q5_K_M.llamafile -> required too much RAM for an average Apple GPU
* models/llava-v1.5-7b-q4.llamafile -> frequently produced empty responses
* gpt4all-falcon-newbpe-q4_0.gguf -> hallucinated on short inputs (when run with llamafile server)
* orca-2-13b.Q4_0.gguf -> produced relatively low change in language style

## Roadmap
* rename 'serve' to 'start'
* secure downloads with checking against hard-coded hashes and/or file size
* publish CLI on PyPi
* add transformation for imitation
