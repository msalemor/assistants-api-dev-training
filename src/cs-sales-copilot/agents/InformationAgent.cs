using agent;
using Azure.AI.OpenAI;

namespace agents;

public class InformationAgent
{
    private InformationAgent() { }

    public static async Task<GPTAgent> GetAgent(AgentSettings? settings,
    OpenAIClient? client)
    {
        var agent = new GPTAgent(settings, client);
        await agent.CreateAgentAsync();
        return agent;
    }
}