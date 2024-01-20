# Adverserial Styolometry LLM

Project to demonstrate the use of LLMs for [adverserial stylometry](https://en.wikipedia.org/wiki/Adversarial_stylometry).

## Model evaluation
### Recommended models
* [mistral-7b-instruct-v0.2.Q3_K_M.llamafile](https://huggingface.co/jartine/Mistral-7B-Instruct-v0.2-llamafile)

### Not recommended models
* models/mistral-7b-instruct-v0.2.Q5_K_S.llamafile -> gave meaningless responses
* mixtral-8x7b-instruct-v0.1.Q5_K_M.llamafile -> required too much RAM
* models/llava-v1.5-7b-q4.llamafile -> sometimes empty responses

## Roadmap

* Automate download of model
* Test more models
* Config for which model to load on startup
* Input dialog (not CLI)
