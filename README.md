# Dryg
Don't Repeat Yourself on GitHub

## Description
**Note** : This is WIP. Only the initial POC is done.

Built using LanceDB + Llama.CPP + GitHub API, dryg aims to:
* Reduce redundant issues for project maintainers and
* Assist users with bugs without having to leave the terminal windows

### Features:
* Works offline (After initial One-Time setup)
* Built on free services with plans to add more embedding APIs like OpenAI and Cohere

## Getting Started
Note: You need to download llama.cpp models from HF here - https://huggingface.co/TheBloke/llama-30b-supercot-GGML/tree/main and put it in `weights/llama-7b.bin` of the working dir. I'll into autamating the model download process but I've not focused on it yet due to license implications.

Dryg setup just requires 3 simple steps:

**Step 1:**
Run `dryg init {username}` to add repos to the database
<img width="735" alt="Screenshot 2023-06-07 at 11 13 32 PM" src="https://github.com/AyushExel/Dryg/assets/15766192/f7634f2c-9c96-4ea3-847f-78443438a65a">
This step builds a lanceDB database for with information about all your public repos and repos from your public orgs
**It syncs with Github API every 7 days**

TODO
- [ ] Allow setting `SYNC_PERIOD` from cli

**Step 2:**
Run `dryg setup {repo_name}` to create issues table of the repo and build search space on LanceDB. It uses LlamaCPP to extract text embeddings.

<img width="732" alt="Screenshot 2023-06-07 at 11 21 57 PM" src="https://github.com/AyushExel/Dryg/assets/15766192/9aba70bf-2b90-466c-9861-1c62d9b05c41">

TODOs:
- [ ] Use issue `body` to build embedding space rather than using `title`: Turn this from PoC to a usable app
- [ ] Make this step redundant by automatically picking up packages from `requirements.txt`, `package.json`, etc.

**Step 3:** 
Paste in your error msg/questions find solutions
<img width="872" alt="Screenshot 2023-06-07 at 11 55 49 PM" src="https://github.com/AyushExel/Dryg/assets/15766192/0fab50d8-0fdb-4caa-87d3-1d385c2daf38">

This is nowhere close to what I initially planned for, but due to the limited contstraint I set for the problem statement

TODOs:
- [ ] Allow maintainers to directly respond to similar issues based on their previous responses to similar issues



Notes/ Analysis/ Takeaways:
* I've built this as a toy example so the search space is built on the `title` of issues rather than the complete `body` of the issue because llama cpp models 1) Don't support large token limit 2) would be very slow to build embedding space for the body
* The performance of 7B llama models is not great for embedding/similarity search and 4-bit quantization makes it suffer more, but it was enough for the MVP version
* It could be because precision doesn't matter too much for generation demos but for embedding space it becomes more important, especially when the semantic meaning of texts are very close by (which it is in this case as issues are from same repo)
Usage
More detailed instructions on how to use your project. This should include code examples, as well as a discussion of the different features and options available.

