from autogen_agentchat.base import TaskResult
from autogen_agentchat.messages import TextMessage

async def run_code_executor_agent(team , docker ,  file_name ,task="simple graph to show prime number" ):
    try:
        # await docker.start()

        task = task + f' and the file is {file_name}'
        async for message in team.run_stream(task = task):
            print('='*200)
            if isinstance(message, TextMessage):
                print("Message from:", message.source)
                print("Content:", message.content)
            elif isinstance(message, TaskResult):
                print (message.stop_reason)
            print('='*200)


    except Exception as e:
        print(f"An error occurred: {e}")
    

async def run_code_executor_agent_streamlit(team, docker, file_name, task="simple graph to show prime number"):
    """
    Streamlit-compatible version of run_code_executor_agent that yields data in a format
    suitable for streaming in a Streamlit app.
    
    Returns:
        An async generator that yields dictionaries with formatted message data
    """
    try:
        await docker.start()

        task = task + f' and the file is {file_name}'
        async for message in team.run_stream(task=task):
            if isinstance(message, TextMessage):
                yield {
                    "type": "message",
                    "source": message.source,
                    "content": message.content,
                    "timestamp": message.timestamp if hasattr(message, "timestamp") else None
                }
            elif isinstance(message, TaskResult):
                yield {
                    "type": "task_result",
                    "stop_reason": message.stop_reason
                }
            else:
                yield {
                    "type": "unknown",
                    "raw_message": str(message)
                }

    except Exception as e:
        yield {
            "type": "error",
            "message": f"An error occurred: {e}"
        }
    finally:
        await docker.stop()
        print("Docker stopped.")
 

