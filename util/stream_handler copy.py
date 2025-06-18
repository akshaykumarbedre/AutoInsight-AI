from autogen_agentchat.messages import (
    TextMessage,
    ToolCallRequestEvent,
    ToolCallExecutionEvent,
)

async def stream_db_conversation(stream_result):
    """
    Generator function to stream database conversation messages
    
    Args:
        stream_result: The async generator from team.run_stream()
        
    Yields:
        Formatted message strings for each step of the conversation
    """
    async for message in stream_result:
        if isinstance(message, TextMessage):
            yield f"💬 {message.source}: {message.content}"
            # yield "-" * 40
        elif isinstance(message, ToolCallRequestEvent):
            for tool_call in message.content:
                yield f"🔧 {message.source} calling tool: {tool_call.name}"
                yield f"   Arguments: {tool_call.arguments}"
            # yield "-" * 40
        elif isinstance(message, ToolCallExecutionEvent):
            for result_item in message.content:
                yield f"✅ Tool '{result_item.name}' executed"
                if result_item.content:
                    content_preview = result_item.content[:100] + "..." if len(result_item.content) > 100 else result_item.content
                    yield f"   Result: {content_preview}"
            
        else:
            yield f"ℹ️ : {type(message).__name__}"
            
    
    yield "CONVERSATION COMPLETED"
    yield message
