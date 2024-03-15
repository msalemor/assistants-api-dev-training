// See https://aka.ms/new-console-template for more information

using Azure;
using Azure.AI.OpenAI.Assistants;
using agent;
using Azure.AI.OpenAI;
using agents;

// Load the settings from the .env file
AgentSettings settings = new();

// Create the C# Assistants client
AssistantsClientOptions options = new(AssistantsClientOptions.ServiceVersion.V2024_02_15_Preview);
AssistantsClient client = new(new Uri(settings.APIEndpoint), new AzureKeyCredential(settings.APIKey), options);
OpenAIClient openAIClient = new(new Uri(settings.APIEndpoint), new AzureKeyCredential(settings.APIKey));

// Create the Sales agent and registration
AssistantAgent salesAgent = await SalesAgent.GetAgent(settings, client);
AgentRegistration salesAgentRegistration = new(salesAgent,
  "SalesIntent",
  "You are an assistant that can answer questions related to customers, sellers, orders and inventory.");

// Create the trading agent and its registration
AssistantAgent cityAgent = await CityAgent.GetAgent(settings, client);
AgentRegistration cityAgentRegistration = new(cityAgent,
  "CityIntent",
  "You are an assistant that answer questions related to favority cities, weather and city nick names.");

// Create a regular GPT agent and its registration
GPTAgent gptAgent = await InformationAgent.GetAgent(settings, openAIClient);
AgentRegistration informationAgentRegistration = new(gptAgent,
  "WeatherIntent",
  "You are an assistant that can provide weather information.");

// Create the proxy and add the registred agents
AgentProxy proxy = new(settings, openAIClient, [salesAgentRegistration, cityAgentRegistration, informationAgentRegistration]);

// Have a conversation with the multi-agent
await proxy.ProcessForIntent("What is the speed of light?");

await proxy.ProcessForIntent("What was the be product sold?");

await proxy.ProcessForIntent("What is Seattle called?");

await proxy.ProcessForIntent("What is the weather in London?");

// Delete the Assistants, Threads and Files used by the agents
await salesAgent.DeleteAsync();
await cityAgent.DeleteAsync();