import azure.functions as func
from datetime import datetime
import json
import logging
import os
from dotenv import load_dotenv
import sales_agent

app = func.FunctionApp()


@app.route(route="AssistantsAPIHttp", methods=['post'], auth_level=func.AuthLevel.ANONYMOUS)
async def AssistantsAPIHttp(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    load_dotenv()

    agent = sales_agent.get_agent()

    name = req.params.get('user_name')
    user_id = req.params.get('user_id')
    prompt = ''

    try:
        req_body = req.get_json()
    except ValueError:
        pass
    else:
        name = req_body.get('user_name')
        user_id = req_body.get('user_id')
        prompt = req_body.get('prompt')

    result = await agent.process_prompt(name, user_id, prompt)

    if result:
        agent.cleanup()
        return func.HttpResponse(
            json.dumps(result),
            mimetype="application/json",
        )
    else:
        return func.HttpResponse(
            "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.",
            status_code=400
        )
