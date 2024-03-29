# Azure OpenAI Assistants API<br/>Thread Message Handling 

## Thread Message Overview 

Assistants API implements several objects including Assistants, Threads, Messages, Runs, and Runs steps.

Threads and Messages are used to track conversations between an Assistant and a user. There is no restriction on the number of Messages that can be stored in a Thread. However, if the Messages become too numerous and exceed the model's context window, the Thread will prioritize including as many recent messages as possible and discard the oldest ones. Messages can contain text, images, or files. 

## How are the Messages stored in a Thread? 

For example, the following two Prompts to the Assistant: 

How do I bake a cake? 

1. Chart y=2x+5, where x=[-10,10]. 
2. Messages can contain text and image references. As the conversation is happening, the Assistant manages the Thread Messages and stores them as follows: 

Messages can contain text and image references. As the conversation is happening, the Assistant manages the Thread Messages and stores them as follows: 

![alt text](images/thread_messages_stack.png)


**Notice:** that as Messages are added in the form of a stack, the last message is the Assistant response from the Assistant for the 2nd Prompt. 

### Annotations 

The content array of the object in Messages from Assistants may have annotations inside. Annotations give information about how to annotate the text in the Message. 
 

There are two types of Annotations: 

- `file_citation`: File citations are made by the retrieval tool and indicate where a certain quote came from in a certain file that was uploaded and used by the Assistant to create the answer. 
- `file_path`: File path annotations are made by the code_interpreter tool and have references to the files that the tool created. 


## Handling Thread Messages when a Run completes 
 
### No Handling 

Retrieve all the Messages from the Thread and bind them in the UI in the exact order as the system returns the messages. 


### Reverse Order 

Retrieve all the Thread Messages to a list, reverse the list order, and bind the list in the UI in the reversed order. 

### Last Message Only 

Let’s look at this Python print_messages function code: 

```python
def read_assistant_file(file_id:str):
    response_content = client.files.content(file_id)
    return response_content.read()

def print_messages(messages: Iterable[MessageFile]) -> None:
    message_list = []

    # Get all the messages till the last user message
    for message in messages:
        message_list.append(message)
        if message.role == "user":
            break

    # Reverse the messages to show the last user message first
    message_list.reverse()

    # Print the user or Assistant messages or images
    for message in message_list:
        for item in message.content:
            # Determine the content type
            if isinstance(item, MessageContentText):
                print(f"{message.role}:\n{item.text.value}\n")
                file_annotations = item.text.annotations
                if file_annotations:
                    for annotation in file_annotations:
                        file_id = annotation.file_path.file_id
                        content = read_assistant_file(file_id)
                        print(f"Annotation Content:\n{str(content)}\n")
            elif isinstance(item, MessageContentImageFile):
                # Retrieve image from file id                
                data_in_bytes = read_assistant_file(item.image_file.file_id)
                # Convert bytes to image
                readable_buffer = io.BytesIO(data_in_bytes)
                image = Image.open(readable_buffer)
                # Resize image to fit in terminal
                width, height = image.size
                image = image.resize((width // 2, height // 2), Image.LANCZOS)
                # Display image
                image.show()
```

This code will: 

- From all the Messages in the Thread, it finds and keeps a local list of Messages until it finds the last user message. 
- Reverses the order of the local list of Messages. 
- For every message on the reversed list, it finds the role and content: 
  - If the content is text, it prints the role and text value. 
  - If the content is an image, it gets the image ID and uses this image ID using the OpenAI client.files to get the image 

In essence, this function returns the last user Prompt first and then the Assistant Messages. 
