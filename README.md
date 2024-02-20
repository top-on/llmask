# LLMask [ɛl ɛl 'ma:sk]

A command-line tool for masking authorship of text,
by changing the writing style with a Large Language Model.

The main use cases of masking an author's writing sytle are:

* anonymizing who is the author of a text
* protecting the identity of whistleblowers and activists
* see more at [Adversarial Stylometry](https://en.wikipedia.org/wiki/Adversarial_stylometry)

## Disclaimer

⚠️ This project currently is just a demo of what LLMs can do for authorship anonymization.<br>
⚠️ There is no strong evidence yet that this tool can beat state of the art de-anonymization methods!

### Known Limitations

Despite it's pre-production status, this library has several known limitations:

1. Only a limited number of transformations are implemented (see `transform.py`).
2. Long chains of transformations have observed to make the LLM output artifacts.
3. Sensitive content can trigger an LLMs censoring, and thus ruin the output.<br>
In this case it is advised to try uncensored LLMs, e.g. of the [`wizard-vicuna-uncensored`](https://registry.ollama.ai/library/wizard-vicuna-uncensored) type.
4. Currently, unique names of places or persons are not removed/anonymized.


## Example workflow

1. Locally serve a Large Language Model server with [ollama](https://ollama.com/):

```
$ ollama serve
```

2. Make sure a potent model is downloaded, e.g. a version of [`nous-hermes2`](https://registry.ollama.ai/library/nous-hermes2):

```
$ ollama pull nous-hermes2:10.7b-solar-q6_K
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

LLMs can run on ordinary CPUs, e.g. with `ollama`.
However, GPU acceleration greatly accelerates execution speed.

This project is best tested on Apple Silicon hardware.

### Installation

This command line tool can be installed with `pipx install`.

### Usage options

```
$ llmask -h

Usage: llmask [OPTIONS]

  Transform input text with chained transformations by a Large Language Model.

Options:
  -t, --transformations TEXT  Compact representation of operations (e.g. 'tsi'
                              for the steps 'thesaurus -> simplify ->
                              imitate')  [default: ts]
  -i, --input TEXT            Input text that will be transformed.  [required]
  -p, --persona TEXT          Name of persona whose writing style to imitate.
                              [default: Ernest Hemingway]
  -m, --model TEXT            Name of model to use (as known to model server).
                              [default: nous-hermes2:10.7b-solar-q6_K]
  -u, --url TEXT              URL of Open AI compatible model API.  [default:
                              http://localhost:11434/v1]
  -h, --help                  Show this message and exit.
```

## Development setup
### Install development environment

The development environment can be installed via: `poetry install`.

### Run test suite

To execute this project's test suite, run `pytest tests/`

## Roadmap
* support transformations from and into text files
* measure success of obfuscation (e.g. check with GPTZero if suspected author is an LLM)
