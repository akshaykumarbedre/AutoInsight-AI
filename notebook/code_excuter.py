import asyncio
from autogen_agentchat.agents import CodeExecutorAgent , AssistantAgent
from autogen_agentchat.messages import UserMessage 
from autogen_ext.code_executors.docker import DockerCommandLineCodeExecutor
from autogen_core import CancellationToken
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.conditions import TextMentionTermination
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")


openai_model_client = OpenAIChatCompletionClient(
    model="gpt-4o",
    api_key=api_key)

code_executor = DockerCommandLineCodeExecutor(work_dir="coding",init_command="pip install pandas", timeout=200)
code_executor_agent = CodeExecutorAgent("code_executor", code_executor=code_executor, model_client=openai_model_client,)
agent = AssistantAgent(
    name="assistant",
    model_client=openai_model_client,
    system_message=(
        "You are a Data Analyst. Your task is to analyze the given data, create a useful graph using matplot, and save it as a PNG image. "
        "If you encounter a ModuleNotFoundError, use a shell script to install the required library using the pip command inline. "
        "Ensure all code is properly formatted in markdown code blocks using triple backticks. For example:\n"
        "```python\nprint(\"Hello World\")\n```\n"
        "or\n"
        "```sh\necho \"Hello World\"\n```\n"
        "Once the graph is generated, ensure it is saved in image format."
    )
)

team=RoundRobinGroupChat(
    participants=[agent, code_executor_agent], 
    
    termination_condition=TextMentionTermination("STOP"),
    

)


async def run_code_executor_agent() -> None:
    # Create a code executor agent that uses a Docker container to execute code.
    try:
        await code_executor.start()

    # Run the agent with a given code snippet.
    
        async for i in team.run_stream(task=" and create simple text pyhon code cheak wheather pandas is working or not  "):
            print(i)
            print("--"*100)
        
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        # Ensure the code executor is stopped even if an error occurs.
        await code_executor.stop()
   


asyncio.run(run_code_executor_agent())
