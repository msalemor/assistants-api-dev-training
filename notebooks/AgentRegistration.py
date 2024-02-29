from AgentSettings import AgentSettings
from openai import AzureOpenAI


class AgentRegistration:
    def __init__(self, settings=None, client=None, intent: str = "intent", intent_desc: str = "intent_desc", agent=None):
        self.settings = settings
        self.client = client
        self.agent = agent
        self.intent = intent
        self.intent_desc = intent_desc

        if settings is None:
            self.settings = AgentSettings()

        if client is None:
            client = AzureOpenAI(
                api_key=self.settings.api_key,
                api_version=self.settings.api_version,
                azure_endpoint=self.settings.api_endpoint)
