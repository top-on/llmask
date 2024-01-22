# Adverserial Styolometry LLM

Project to demonstrate the use of LLMs for [Adversarial Stylometry](https://en.wikipedia.org/wiki/Adversarial_stylometry).

The main use cases of Adversarial Stylometry are:

* obfuscating and anonymizing a text's author
* protecting the identity of whistleblowers and activists

## Disclaimer

⚠️ This project currently is just a demo on what LLMs can do for authorship anonymization.<br>
⚠️ There is no proof that this tool can beat state-of-the-art stylometry!

### Known Limitations

Despite it's pre-production status, this library has several known limitations:

1. Only a limited number of transformations are implemented (see `transform.py`).
2. Long chains of transformations have observed to make the LLM output artifacts.

## Example usage

On the terminal, this tool takes in text and transforms it to 

```
$ asllm  -i "our sun is shining soo bright on this lecker morning."

The sun shines very brightly on this lovely morning.
```

## Getting started
### System requirements

This library is tested on *Apple Silicon*, but it is expected to run on x86, too.

### Installation

This tool can be installed with `poetry install`.

### Usage options

```
$ asllm -h
Usage: asllm [OPTIONS]

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
* add open license
* automate server startup from CLI
* publish CLI on PyPi
* add transformation for imitation
* Test more models
* Config for which model to load on startup
