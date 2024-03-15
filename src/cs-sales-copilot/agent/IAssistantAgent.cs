namespace agent;
using Azure.AI.OpenAI.Assistants;

public interface IAssistantAgent
{
    public Task CreateAgentAsync();
    public Task LoadFilesAsync(string folderPath);
    public Task<BinaryData> GetFileContent(string id);
    public Task ProcessMessagesAsync(IReadOnlyList<ThreadMessage> messages);
    public Task ProcessPromptAsync(string input, int maxTokens = 100, float temperature = 0.3f);
    public Task DeleteAsync();
}
