
# Overview 
A helpful command line assistant, based on ChatGPT.

# Getting started
Install Zed by running: 
```bash
pip install zed-assistant
```
Note that Zed requires Python 3.8+.

You'll need your own OpenAI key to be able to use Zed. The key can be configured as an environment variable or  passed as a command parameter:
```
echo "export ZED_OAI_KEY=my-key" >> ~/.zshrc  # or .bash_profile, etc
```

# Usage
Run `zed` with no arguments to get the help menu:
```
~ zed

     ______ ___________
    |___  /|  ___|  _  \
       / / | |__ | | | |
      / /  |  __|| | | |
    ./ /___| |___| |/ /
    \_____/\____/|___/

usage: zed [-h] [--debug] [--model {gpt-4,gpt-4-turbo,gpt-3.5-turbo}] [--open-ai-key OPEN_AI_KEY]

zed is a LLM-based CLI assistant built with python and Chat GPT

optional arguments:
  -h, --help            show this help message and exit
  --debug               Enables print debug logs.
  --model {gpt-4,gpt-4-turbo,gpt-3.5-turbo}
                        The specific Open AI model to be used. Default is 'gpt-4-turbo'.
  --open-ai-key OPEN_AI_KEY
                        The Open AI API key. You can also set the environment variable ZED_OAI_KEY.
```

# Contributing 
## Install dependencies
Setup the project locally:
```bash
git clone https://github.com/hoffmannmatheus/zed/ && cd zed
poetry install
```

## Run tests
```bash
poetry run pytest
```

## Run zed locally
First, setup your local OpenAI API key: 
```bash
export ZED_OAI_KEY="your-openai-key"
```
Then, run locally with:
```bash
poetry run zed
```

## Publishing a new version
```bash
poetry publish --build
```
