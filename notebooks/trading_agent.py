import common

from AgentSettings import AgentSettings
from AssistantAgent import AssistantAgent
from openai import AzureOpenAI


def call_functions(client, thread, run):
    print("Function Calling")
    required_actions = run.required_action.submit_tool_outputs.model_dump()
    print(required_actions)
    tool_outputs = []
    import json
    for action in required_actions["tool_calls"]:
        func_name = action['function']['name']
        arguments = json.loads(action['function']['arguments'])

        if func_name == "get_stock_price":
            output = common.get_stock_price(symbol=arguments['symbol'])
            tool_outputs.append({
                "tool_call_id": action['id'],
                "output": output
            })
        elif func_name == "send_email":
            print("Sending email...")
            email_to = arguments['to']
            email_content = arguments['content']
            common.send_logic_apps_email(email_to, email_content)

            tool_outputs.append({
                "tool_call_id": action['id'],
                "output": "Email sent"
            })
        else:
            raise ValueError(f"Unknown function: {func_name}")

    print("Submitting outputs back to the Assistant...")
    client.beta.threads.runs.submit_tool_outputs(
        thread_id=thread.id,
        run_id=run.id,
        tool_outputs=tool_outputs
    )


tools_list = [
    {"type": "code_interpreter"},
    {"type": "function",
        "function": {
            "name": "get_stock_price",
            "description": "Retrieve the latest closing price of a stock using its ticker symbol.",
            "parameters": {
                "type": "object",
                "properties": {
                    "symbol": {
                        "type": "string",
                        "description": "The ticker symbol of the stock"
                    }
                },
                "required": ["symbol"]
            }
        }
     },
]

DATA_FOLDER = None


def get_agent(settings=None, client=None):

    if settings is None:
        settings = AgentSettings()

    if client is None:
        client = AzureOpenAI(
            api_key=settings.api_key,
            api_version=settings.api_version,
            azure_endpoint=settings.api_endpoint)

    agent = AssistantAgent(settings,
                           client,
                           "Trading Agent", "You are an agent that can help get the latest stock prices and perform investment related calculations.",
                           DATA_FOLDER, tools_list, fn_calling_delegate=call_functions)

    return agent
