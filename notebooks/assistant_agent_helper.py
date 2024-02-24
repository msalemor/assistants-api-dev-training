import os
import time
import shelve

from threading import Lock
from datetime import datetime
from pathlib import Path
from typing import Iterable

from dotenv import load_dotenv
from openai import AzureOpenAI
from openai.types import FileObject
from openai.types.beta import Thread
from openai.types.beta.threads import Run
from openai.types.beta.threads.message_content_image_file import MessageContentImageFile
from openai.types.beta.threads.message_content_text import MessageContentText
from openai.types.beta.threads.messages import MessageFile
from PIL import Image

# Keep a list of the assistants
ai_assistants = []
# List of threads created
ai_threads = []
# List of files uploaded
ai_files = []
#
assistant = None

# client = AzureOpenAI(
#     api_key=api_key, api_version=api_version, azure_endpoint=api_endpoint)

tools_list = [
    {"type": "code_interpreter"}
]

DATA_FOLDER = "data/sales/"


def upload_file(client: AzureOpenAI, path: str) -> FileObject:
    print(path)
    with Path(path).open("rb") as f:
        return client.files.create(file=f, purpose="assistants")


def read_assistant_file(client, file_id: str):
    response_content = client.files.content(file_id)
    return response_content.read()


def upload_all_files(client, folder: str):
    files = os.listdir(folder)
    assistant_files = []
    for file in files:
        filePath = DATA_FOLDER + file
        assistant_file = upload_file(client, filePath)
        ai_files.append(assistant_file)
        assistant_files.append(assistant_file)
    return [file.id for file in assistant_files]


def add_thread(thread):
    for item in ai_threads:
        if item.id == thread.id:
            return
    ai_threads.append(thread)
    print("Added thread: ", thread.id, len(ai_threads))


def check_if_thread_exists(user_id):
    with shelve.open("threads_db") as threads_shelf:
        return threads_shelf.get(user_id, None)


def store_thread(user_id, thread):
    with shelve.open("threads_db", writeback=True) as threads_shelf:
        add_thread(thread)
        threads_shelf[user_id] = thread.id


def clear_shelves():
    with shelve.open("assistant_db") as assistant_shelf:
        assistant_shelf.clear()
    with shelve.open("threads_db") as threads_shelf:
        threads_shelf.clear()


# clear_shelves()


def get_sales_assistant(client, model_deployment, name, instructions, tools_list, folder):
    clear_shelves()
    assistant = client.beta.assistants.create(
        name=name,  # "Sales Assistant",
        # "You are a sales assistant. You can answer questions related to customer orders.",
        instructions=instructions,
        tools=tools_list,
        model=model_deployment,
        file_ids=upload_all_files(client, folder),
    )
    ai_assistants.append(assistant)
    assistant = assistant
    return assistant


def print_messages(name: str, messages: Iterable[MessageFile]) -> None:
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
                if message.role == "user":
                    print(f"user: {name}:\n{item.text.value}\n")
                else:
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


def process_prompt(client, assistant, name: str, user_id: str, prompt: str, keep_state: bool = False, delegate=None) -> None:

    if keep_state:
        thread_id = check_if_thread_exists(user_id)

        # If a thread doesn't exist, create one and store it
        if thread_id is None:
            print(f"Creating new thread for {name} with user_id {user_id}")
            thread = client.beta.threads.create()
            store_thread(user_id, thread)
            thread_id = thread.id
        # Otherwise, retrieve the existing thread
        else:
            print(
                f"Retrieving existing thread for {name} with user_id {user_id}")
            thread = client.beta.threads.retrieve(thread_id)
            add_thread(thread)
    else:
        thread = client.beta.threads.create()

    client.beta.threads.messages.create(
        thread_id=thread.id, role="user", content=prompt)

    run = client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=assistant.id,
        instructions="Please address the user as Jane Doe. The user has a premium account. Be assertive, accurate, and polite. Ask if the user has further questions. Do not provide explanations for the answers."
        + "The current date and time is: "
        + datetime.now().strftime("%x %X")
        + ". ",
    )

    print("processing ...")
    while True:
        run = client.beta.threads.runs.retrieve(
            thread_id=thread.id, run_id=run.id)
        if run.status == "completed":
            # Handle completed
            messages = client.beta.threads.messages.list(thread_id=thread.id)
            print_messages(name, messages)
            break
        if run.status == "failed":
            messages = client.beta.threads.messages.list(thread_id=thread.id)
            print_messages(name, messages)
            # Handle failed
            break
        if run.status == "expired":
            # Handle expired
            break
        if run.status == "cancelled":
            # Handle cancelled
            break
        if run.status == "requires_action":
            if delegate:
                delegate(client, thread, run)
        else:
            time.sleep(5)
    if keep_state:
        client.beta.threads.delete(thread.id)
        print("Deleted thread: ", thread.id)


def cleanup(client):
    print("Deleting: ", len(ai_assistants), " assistants.")
    for assistant in ai_assistants:
        print(client.beta.assistants.delete(assistant.id))
    print("Deleting: ", len(ai_threads), " threads.")
    for thread in ai_threads:
        print(client.beta.threads.delete(thread.id))
    print("Deleting: ", len(ai_files), " files.")
    for file in ai_files:
        print(client.files.delete(file.id))


class CKVStore:
    def __init__(self):
        self.list = []
        self.lock = Lock()

    def get_category(self, category):
        return [item for item in self.list if item["category"] == category]

    def get_value(self, category, key):
        return [item["value"] for item in self.list if item["category"] == category and item["key"] == key]

    def upsert_value(self, category, key, value):
        for item in self.list:
            if item["category"] == category and item["key"] == key and item["value"] == value:
                # item["value"] = value
                return
        with self.lock:
            self.list.append(
                {"category": category, "key": key, "value": value})

    def delete_category(self, category):
        with self.lock:
            self.list = [
                item for item in self.list if item["category"] != category]

    def delete_key(self, category, key, value):
        with self.lock:
            self.list = [
                item for item in self.list if not (item["category"] == category and item["key"] == key and item["value"] == value)]

    def reset(self):
        with self.lock:
            self.list = []
