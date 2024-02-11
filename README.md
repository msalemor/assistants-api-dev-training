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

- GPT models are restful endpoint:
  - `POST /completion`
- Assistants API extended these models with:
  - `POST/GET/DELETE /assistant`
  - `POST/GET/DELETE /thread`
  - `POST/GET/DELETE /run`
  - `POST/GET/DELETE /message`

## Tools

| Feature | Description |
|----------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Code Interpreter | Allows the Assistants API to write and run Python code in a sandboxed execution environment. This tool can process files with diverse data and formatting, and generate files with data and images of graphs. |
| Function Calling | Allows you to describe functions to the Assistants and have it intelligently return the functions that need to be called along with their arguments. The Assistants API will pause execution during a Run when it invokes functions, and you can supply the results of the function call back to continue the Run execution. |
| Knowledge Retrieval | Retrieval augments the Assistant with knowledge from outside its model, such as proprietary product information or documents provided by your users. Once a file is uploaded and passed to the Assistant, OpenAI will automatically chunk your documents, index and store the embeddings, and implement vector search to retrieve relevant content to answer user queries. |

## Objects

| Object | Description |
|-------------|------------------------------------------------------------------------------------------------------------------------|
| Assistant | Purpose-built AI that uses OpenAI’s models and calls tools |
| Thread | A conversation session between an Assistant and a user. Threads store Messages and automatically handle truncation. |
| Message | A message created by an Assistant or a user. Messages can include text, images, and other files. Stored as a list. |
| Run | An invocation of an Assistant on a Thread. The Assistant uses its configuration and the Thread’s Messages to perform tasks. |
| Run Step | A detailed list of steps the Assistant took as part of a Run. Allows introspection of how the Assistant achieves results. |

## Run Lifecycle

| Status | Description |
|--------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| queued | When Runs are first created or when you complete the required_action, they are moved to a queued status. They should almost immediately move to in_progress. |
| in_progress | While in_progress, the Assistant uses the model and tools to perform steps. You can view the progress being made by the Run by examining the Run Steps. |
| completed | The Run successfully completed! You can now view all Messages the Assistant added to the Thread, and all the steps the Run took. You can also continue the conversation by adding more user Messages to the Thread and creating another Run. |
| requires_action | When using the Function calling tool, the Run will move to a required_action state once the model determines the names and arguments of the functions to be called. You must then run those functions and submit the outputs before the run proceeds. If the outputs are not provided before the expires_at timestamp passes (roughly 10 minutes past creation), the run will move to an expired status. |
| expired | This happens when the function calling outputs were not submitted before expires_at and the run expires. Additionally, if the runs take too long to execute and go beyond the time stated in expires_at, our systems will expire the run. |
| cancelling | You can attempt to cancel an in_progress run using the Cancel Run endpoint. Once the attempt to cancel succeeds, the status of the Run moves to cancelled. Cancellation is attempted but not guaranteed. |
| cancelled | Run was successfully cancelled. |
| failed | You can view the reason for the failure by looking at the last_error object in the Run. The timestamp for the failure will be recorded under failed_at. |

## Usual flow

- Create an Assistant in the API by defining its custom instructions and picking a model. If helpful, enable tools like Code Interpreter, Retrieval, and Function calling.
- Create a Thread when a user starts a conversation.
- Add Messages to the Thread as the user asks questions.
- Run the Assistant on the Thread to trigger responses. This automatically calls the relevant tools.

## Thread Messages Handling

For example, if a user sends two Prompt to the Assistant:

1. Can you give me a recipe to bake a cake?
2. Can you chart y=2*x+5, where x=[-10,10]?

As the conversation is happening, the Assistant manages the Thread Messages and stores them as follows:

| Role | Type | Message |
|------|------|---------|
| assistant | Image | File_id to PNG image |
| assistant | Text | Here’s your chart |
| user | Text | Can you chart y=2*x+5, where x=[-10,10]? |
| assistant | Text | Pour into a mold and bake at 350F for 45 minutes. |
| assistant | Text | To bake a cake, blend a cup of flour, a cup of milk, half a cup of sugar, and a tablespoon of vanilla. |
| assistant | Text | I can do that. |
| user | Text | Can you give me a recipe to bake a cake? |

## Cleanup
