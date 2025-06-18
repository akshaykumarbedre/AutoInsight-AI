from autogen_agentchat.messages import (
    TextMessage,
    ToolCallRequestEvent,
    ToolCallExecutionEvent,
)

async def stream_db_conversation(stream_result):
    """
    Generator function to stream database conversation messages with enhanced UX
    
    Args:
        stream_result: The async generator from team.run_stream()
        
    Yields:
        Formatted message dictionaries for better UI rendering
    """
    async for message in stream_result:
        if isinstance(message, TextMessage):
            # Enhanced text message formatting
            yield {
                "type": "text",
                "source": message.source,
                "content": message.content,
                "emoji": "🤖" if "Database" in message.source else "🎨",
                "timestamp": True
            }
        elif isinstance(message, ToolCallRequestEvent):
            # Tool call request with better formatting
            for tool_call in message.content:
                yield {
                    "type": "tool_request",
                    "source": message.source,
                    "tool_name": tool_call.name,
                    "arguments": tool_call.arguments,
                    "emoji": "🔧",
                    "timestamp": True
                }
        elif isinstance(message, ToolCallExecutionEvent):
            # Tool execution results with preview
            for result_item in message.content:
                content_preview = ""
                if result_item.content:
                    content_preview = result_item.content[:250] + "..." if len(result_item.content) > 250 else result_item.content
                
                yield {
                    "type": "tool_result",
                    "tool_name": result_item.name,
                    "content": content_preview,
                    "emoji": "✅",
                    "timestamp": True
                }
        else:
            # Other message types
            yield {
                "type": "system",
                "content": f"Processing: {type(message).__name__}",
                "emoji": "ℹ️",
                "timestamp": True
            }
    
    # Completion indicator
    yield {
        "type": "completion",
        "content": "Task completed successfully",
        "emoji": "🎉",
        "timestamp": True
    }
    yield message
