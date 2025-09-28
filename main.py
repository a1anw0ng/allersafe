import litellm
import json

print("Starting Allergy Detector...")

# Define a tool
tools = [{
    "type": "function",
    "function": {
        "name": "get_weather",
        "description": "Get the weather",
        "parameters": {
            "type": "object",
            "properties": {
                "location": {"type": "string"}
            },
            "required": ["location"]
        }
    }
}]
print(f"Tools defined: {len(tools)} available")

def get_weather(location):
    print(f"get_weather called with: {location}")
    result = f"The weather in {location} is sunny"
    print(f"get_weather result: {result}")
    return result

print("Making API call...")
try:
    response = litellm.completion(
        model="gpt-5",
        messages=[{"role": "user", "content": "What's the weather in NYC?"}], # User message
        tools=tools # Loads up description of tools
    )
    print("API call successful")
    
    message = response.choices[0].message
    print(f"Response content: {message.content}")
    
    # Print tool call if it happened
    if hasattr(message, 'tool_calls') and message.tool_calls:
        print(f"Tool calls detected: {len(message.tool_calls)}")
        
        for tool_call in message.tool_calls:
            print(f"Tool: {tool_call.function.name}")
            print(f"Args: {tool_call.function.arguments}")
            
            # Execute the tool
            if tool_call.function.name == "get_weather":
                args_dict = json.loads(tool_call.function.arguments)
                result = get_weather(args_dict.get("location", "unknown"))
    else:
        print("No tool calls detected")

except Exception as e:
    print(f"Error: {e}")

print("Done.")