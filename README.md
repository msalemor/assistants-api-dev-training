# Assistants API - Development Concepts

An Assistants API development training

## Overview

The Assistants API allows you to build AI assistants within your own applications. An Assistant has instructions and can leverage models, tools, and knowledge to respond to user queries.

## Objective

- To define what Assistants API is
- To introduce the Assistants API development concepts
- Compare a Jupyter notebook written without Assistants API and with Assistants API
- Look at a full demo app
- Understand the Assistant API foundational concepts, limits, use cases

## What is Assistants API

- GPT models are restful endpoint
  - Generally, GPT endpoints provide the `POST /completion` endpoint
- Assistants API extended these models with:
  - `POST/GET/DELETE /assistant`
  - `POST/GET/DELETE /thread`
  - `POST/GET/DELETE /run`
  - `POST/GET/DELETE /message`

## Assistants API comes with tools

- Code Interpreter: Allows the Assistants API to write and run Python code in a sandboxed execution environment. This tool can process files with diverse data and formatting, and generate files with data and images of graphs.
- Function Calling: Allows you to describe functions to the Assistants and have it intelligently return the functions that need to be called along with their arguments. The Assistants API will pause execution during a Run when it invokes functions, and you can supply the results of the function call back to continue the Run execution.
- Knowledge Retrieval: Retrieval augments the Assistant with knowledge from outside its model, such as proprietary product information or documents provided by your users. Once a file is uploaded and passed to the Assistant, OpenAI will automatically chunk your documents, index and store the embeddings, and implement vector search to retrieve relevant content to answer user queries.

## Usual flow

- Create an Assistant in the API by defining its custom instructions and picking a model. If helpful, enable tools like Code Interpreter, Retrieval, and Function calling.
- Create a Thread when a user starts a conversation.
- Add Messages to the Thread as the user ask questions.
- Run the Assistant on the Thread to trigger responses. This automatically calls the relevant tools.

## Event Loop

## Message Handling

## Cleanup
