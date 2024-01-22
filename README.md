# LLMask [ɛl ɛl 'ma:sk]

A command-line tool for masking authorship of a text,
by changing its writing style with a Large Language Model.

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

1. Download Large Language Model:

```
llmask download
```

2. Serve downloaded model on your local machine (keep terminal open while serving):

```
llmask serve
```

3. Transform your own writing style into a different one:

```
$ llmask transform --input "our sun is shining soo bright on this lecker morning."

The sun shines very brightly on this lovely morning.
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

This project uses the LLM [mistral-7b-instruct-v0.2.Q3_K_M.llamafile](https://huggingface.co/jartine/Mistral-7B-Instruct-v0.2-llamafile).

Some other models have been evaluated negatively, for different reasons:
* models/mistral-7b-instruct-v0.2.Q5_K_S.llamafile - gave meaningless/confused responses
* mixtral-8x7b-instruct-v0.1.Q5_K_M.llamafile - required too much RAM for an average Apple GPU
* models/llava-v1.5-7b-q4.llamafile -> frequently produced empty responses

## Roadmap
* traceable output (see TODO in CLI module)
* add code quality checks (ruff, mypy, pre-commit)
* publish CLI on PyPi
* add transformation for imitation
* Test more models
* Config for which model to load on startup
