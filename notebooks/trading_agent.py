import custom_assistant

tools_list = [
    {"type": "code_interpreter"}
]

DATA_FOLDER = "data/sales/"


def get_sales_assistant():
    return custom_assistant.AssistantAgent(DATA_FOLDER, tools_list)
