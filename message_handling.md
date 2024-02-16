# Azure OpenAI Assistants API<br/>Thread Message Handling 

## Overview 

In Assistants API, Threads and Messages are used to track conversations between an Assistant and a user. There is no restriction on the number of Messages that can be stored in a Thread. However, if the Messages become too numerous and exceed the model's context window, the Thread will prioritize including as many recent messages as possible and discard the oldest ones. Messages can contain text, images, or files. 

## Assistants API Objects 

Component 

Description 

Assistant 

Custom AI that uses Azure OpenAI models in conjunction with tools. 

Thread 

A conversation session between an Assistant and a user. Threads store Messages and automatically handle truncation to fit content into a model’s context. 

Message 

A message created by an Assistant or a user. Messages can include text, images, and other files. Messages are stored as a list on the Thread. 

Run 

Activation of an Assistant to begin running based on the contents of the Thread. The Assistant uses its configuration and the Thread’s Messages to perform tasks by calling models and tools. As part of a Run, the Assistant appends Messages to the Thread. 

Run Step 

A detailed list of steps the Assistant took as part of a Run. An Assistant can call tools or create Messages during it’s run. Examining Run Steps allows you to understand how the Assistant is getting to its final results. 


## How are the Messages stored in a Thread? 

For example, if a user sends two Prompt to the Assistant: 

How do I bake a cake? 

Chart y=2x+5, where x=[-10,10]. 

Messages can contain text and image references. As the conversation is happening, the Assistant manages the Thread Messages and stores them as follows: 



 

**> Notice:** that as Messages are added in the form of a stack, the last message is the Assistant response from the Assistant for the 2nd Prompt. 

 

### Annotations 

The content array of the object in Messages from Assistants may have annotations inside. Annotations give information about how to annotate the text in the Message. 

 

There are two types of Annotations: 

file_citation: File citations are made by the retrieval tool and indicate where a certain quote came from in a certain file that was uploaded and used by the Assistant to create the answer. 

file_path: File path annotations are made by the code_interpreter tool and have references to the files that the tool created. 

 

## Handling Thread Messages when a Run completes 
 
### No Handling 

Retrieve all the Messages from the Thread and bind them in the UI in the exact order as the system returns the messages. 


### Reverse Order 

Retrieve all the Thread Messages to a list, reverse the list order, and bind the list in the UI in the reversed order. 

### Last Message Only 

Let’s look at this Python code: 




 

This code will: 

From all the Messages in the Thread, it finds and keeps a local list of Messages until it finds the last user message. 

Reverses the order of the local list of Messages. 

For every message on the reversed list, it finds the role and content: 

If the content is text, it prints the role, text value. 

If the content is an image, it gets the image ID and uses this image ID using the OpenAI client.files to get the image 

In essence, this function returns the last user Prompt first and then the Assistant Messages. 
