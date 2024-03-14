// See https://aka.ms/new-console-template for more information

using Azure;
using Azure.AI.OpenAI.Assistants;
using agent;

// Load the settings from the .env file
AgentSettings settings = new();

// Create the C# Assistants client
AssistantsClientOptions options = new(AssistantsClientOptions.ServiceVersion.V2024_02_15_Preview);
AssistantsClient client = new(new Uri(settings.APIEndpoint), new AzureKeyCredential(settings.APIKey), options);

// Create the Sales agent and registration
AssistantAgent salesAgent = await SalesAgent.SalesAgent.GetAgent(settings, client);
AgentRegistration salesAgentRegistration = new(salesAgent,
  "SalesIntent",
  "You are an assistant that can answer questions related to customers, sellers, orders and inventory.");

// Create the trading agent and its registration
AssistantAgent informationAgent = await InformationAgent.InformationAgent.GetAgent(settings, client);
AgentRegistration tradingAgentRegistration = new(informationAgent,
  "CityWeatherIntent",
  "You are an assistant that answer questions related to favority cities, weather and city nick names.");

// Create the proxy and add the registred agents
AgentProxy proxy = new(settings, [salesAgentRegistration, tradingAgentRegistration]);

// Have a conversation with the multi-agent
await proxy.ProcessForIntent("What is the speed of light?");

await proxy.ProcessForIntent("What was the be product sold?");

await proxy.ProcessForIntent("What is Seattle called?");

// Delete the Assistants, Threads and Files used by the agents
await salesAgent.DeleteAsync();
await informationAgent.DeleteAsync();