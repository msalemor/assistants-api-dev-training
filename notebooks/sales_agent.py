from assistant_agent import AssistantAgent
from openai import AzureOpenAI

from assistant_agent_settings import AgentSettings

tools_list = [
    {"type": "code_interpreter"}
]

DATA_FOLDER = "data/sales/"

settings = AgentSettings()

client = AzureOpenAI(
    api_key=settings.api_key,
    api_version=settings.api_version,
    azure_endpoint=settings.api_endpoint)


def get_agent():
    agent = AssistantAgent(settings,
                           client,
                           "Sales Assistant", "You are an Assistant that can help answer questions and perform calculations related to customers, customer orders, inventory, and sellers with the provided CSV files.", DATA_FOLDER, tools_list)
    agent.get_agent()
    return agent
