namespace agent;

public class AgentRegistration(IAssistantAgent agent, string intent, string intentDescription)
{
    public IAssistantAgent Agent { get; set; } = agent;
    public string Intent { get; set; } = intent;
    public string IntentDescription { get; set; } = intentDescription;
}