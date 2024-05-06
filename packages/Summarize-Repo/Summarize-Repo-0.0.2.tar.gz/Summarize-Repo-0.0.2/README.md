# Overview
Summarize Repo is the quickest solution for repository analysis.

## Installation
You can easily install Summarize Repo via pip:

```
pip install summarize-repo
```

## Usage
By analyzing filenames, Summarize Repo can infer the nature of the repository. 

Summarize can be used directly from the command line:

```
>>> ask <dir>
Based on the filenames in the repository, it appears to be a web development project using JavaScript. "App.js" suggests a main application file, while "important.py" could be a script for crucial functionalities. The folder structure and file naming indicate a frontend project structure.
```

## Clone this repo
```
git clone https://github.com/mlekhi/summarize.git
```
Go to the root folder
```
cd summarize-repo
```
Install Summarize Repo in the directory using "editable" mode. This ensures that any modifications made will automatically update the package without requiring a fresh installation. If Summarize Repo is already installed, uninstall it prior to this step:
```
(if needed) pip uninstall summarize-repo
pip install -e .
```

Now, you can freely modify the source code and continue using the "ask" CLI command across your system with your custom version of Summarize Repo.

### Using a Different Language Model (LLM)
We encourage users to experiment and enhance Summarize Repo's functionality.

The "llm.py" file serves as a playground for creating custom endpoint functions. For instance, incorporating an OLLAMA_client could be a promising addition.

To utilize a different LLM, like Groq, run:
```
ask --llm=groq
```

Please note that this requires providing API keys via environment variables. Refer to .env.example for guidance on setting them in a .env file or through your shell startup script (~/.bashrc, ~/.zshrc, etc.).

## Licensing
Summarize Repo is licensed under the MIT License. For more details, refer to the LICENSE file.
