namespace agent;

using System.Diagnostics.CodeAnalysis;
using System.Text;
using System.Text.Json;
using Azure;
using Azure.AI.OpenAI;
using Azure.AI.OpenAI.Assistants;
public class GPTAgent : IAssistantAgent
{
    public AgentSettings Settings { get; set; }
    public OpenAIClient Client { get; set; }
    public List<ToolDefinition> Tools { get; set; }
    public List<string> FileIds { get; set; }
    public Assistant Assistant { get; set; } = null!;
    public AssistantThread Thread { get; set; } = null!;
    public string? DataFolder { get; set; }

    public delegate ToolOutput? ResolveOutputDelegate(RequiredToolCall toolCall);
    public ResolveOutputDelegate? GetResolvedToolOutput { get; set; }


    public GPTAgent(AgentSettings? settings, OpenAIClient? client, List<ToolDefinition>? tools = null, List<string>? fileIds = null, string? dataFolder = null, ResolveOutputDelegate? resolveDelegate = null)
    {
        // (AgentSettings? settings, AssistantsClient? client, string name, string instructions)
        Settings = settings ?? new AgentSettings();
        Client = client ?? new OpenAIClient(new Uri(Settings.APIEndpoint), new AzureKeyCredential(Settings.APIKey));
        Tools = tools ?? [new CodeInterpreterToolDefinition()];
        FileIds = fileIds ?? [];
        DataFolder = dataFolder;
        GetResolvedToolOutput = resolveDelegate;
    }

    public async Task LoadFilesAsync(string folderPath)
    {
        await Task.Delay(1);
    }

    public async Task CreateAgentAsync()
    {
        // TODO: Remove
        await Task.Delay(1);
    }

    public async Task<BinaryData> GetFileContent(string id)
    {
        await Task.Delay(1);
        return null!;
    }

    public async Task ProcessMessagesAsync(IReadOnlyList<ThreadMessage> messages)
    {
        await Task.Delay(1);
    }

    // public void Resolve(RequiredToolCall call) {
    //     if (GetResolvedToolOutput is null)
    //     {
    //         GetResolvedToolOutput = GetResolvedToolOutput(call);
    //     }
    // }

    // ToolOutput? GetResolvedToolOutput(RequiredToolCall toolCall)
    // {
    //     if (toolCall is RequiredFunctionToolCall functionToolCall)
    //     {
    //         if (functionToolCall.Name == InformationAgent.InformationAgent.getUserFavoriteCityTool.Name)
    //         {
    //             return new ToolOutput(toolCall, InformationAgent.InformationAgent.GetUserFavoriteCity());
    //         }
    //         using JsonDocument argumentsJson = JsonDocument.Parse(functionToolCall.Arguments);
    //         if (functionToolCall.Name == InformationAgent.InformationAgent.getCityNicknameTool.Name)
    //         {
    //             string locationArgument = argumentsJson.RootElement.GetProperty("location").GetString() ?? "";
    //             return new ToolOutput(toolCall, InformationAgent.InformationAgent.GetCityNickname(locationArgument));
    //         }
    //         if (functionToolCall.Name == InformationAgent.InformationAgent.getCurrentWeatherAtLocationTool.Name)
    //         {
    //             string locationArgument = argumentsJson.RootElement.GetProperty("location").GetString() ?? "";
    //             if (argumentsJson.RootElement.TryGetProperty("unit", out JsonElement unitElement))
    //             {
    //                 string? unitArgument = unitElement.GetString() ?? "";
    //                 return new ToolOutput(toolCall, InformationAgent.InformationAgent.GetWeatherAtLocation(locationArgument, unitArgument));
    //             }
    //             return new ToolOutput(toolCall, InformationAgent.InformationAgent.GetWeatherAtLocation(locationArgument));
    //         }
    //     }
    //     return null;
    // }

    // Purely for convenience and clarity, this standalone local method handles tool call responses.
    ChatRequestToolMessage GetToolCallResponseMessage(ChatCompletionsToolCall toolCall)
    {
        var functionToolCall = toolCall as ChatCompletionsFunctionToolCall;
        if (functionToolCall?.Name == "get_current_weather")
        {
            // Validate and process the JSON arguments for the function call
            string unvalidatedArguments = functionToolCall.Arguments;
            var functionResultData = (object)null; // GetYourFunctionResultData(unvalidatedArguments);
            // Here, replacing with an example as if returned from "GetYourFunctionResultData"
            functionResultData = "31 celsius";
            return new ChatRequestToolMessage(functionResultData.ToString(), toolCall.Id);
        }
        else
        {
            // Handle other or unexpected calls
            throw new NotImplementedException();
        }
    }

    public async Task ProcessPromptAsync(string input, int maxTokens = 100, float temperature = 0.3f)
    {
        var getWeatherTool = new ChatCompletionsFunctionToolDefinition()
        {
            Name = "get_current_weather",
            Description = "Get the current weather in a given location",
            Parameters = BinaryData.FromObjectAsJson(
            new
            {
                Type = "object",
                Properties = new
                {
                    Location = new
                    {
                        Type = "string",
                        Description = "The city and state, e.g. San Francisco, CA",
                    },
                    Unit = new
                    {
                        Type = "string",
                        Enum = new[] { "celsius", "fahrenheit" },
                    }
                },
                Required = new[] { "location" },
            },
            new JsonSerializerOptions() { PropertyNamingPolicy = JsonNamingPolicy.CamelCase }),
        };

        var chatCompletionsOptions = new ChatCompletionsOptions()
        {
            DeploymentName = Settings.APIDeploymentName, // Use DeploymentName for "model" with non-Azure clients            
            MaxTokens = maxTokens,
            Temperature = temperature,
            Tools = { getWeatherTool }
        };
        chatCompletionsOptions.Messages.Add(new ChatRequestAssistantMessage(input));

        try
        {
            //Response<ChatCompletions> response = await Client.GetChatCompletionsAsync(chatCompletionsOptions);
            Response<ChatCompletions> response = await Client.GetChatCompletionsAsync(chatCompletionsOptions);
            ChatChoice responseChoice = response.Value.Choices[0];
            if (responseChoice.FinishReason == CompletionsFinishReason.ToolCalls)
            {
                // Add the assistant message with tool calls to the conversation history
                ChatRequestAssistantMessage toolCallHistoryMessage = new(responseChoice.Message);
                chatCompletionsOptions.Messages.Add(toolCallHistoryMessage);

                // Add a new tool message for each tool call that is resolved
                foreach (ChatCompletionsToolCall toolCall in responseChoice.Message.ToolCalls)
                {
                    chatCompletionsOptions.Messages.Add(GetToolCallResponseMessage(toolCall));
                }

                // Now make a new request with all the messages thus far, including the original
                response = await Client.GetChatCompletionsAsync(chatCompletionsOptions);
                Console.WriteLine(response.Value.Choices[0].Message.Content);
            }

        }
        catch (Exception)
        {
            Console.WriteLine();
        }
    }

    public async Task DeleteAsync()
    {
        await Task.Delay(1);
    }
}
