
from autogen_agentchat.agents import CodeExecutorAgent
from autogen_ext.code_executors.docker import DockerCommandLineCodeExecutor
from autogen_agentchat.messages import TextMessage
from autogen_core import CancellationToken
import asyncio
from autogen_agentchat.agents import AssistantAgent , UserProxyAgent
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_core.tools import FunctionTool
import os
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.teams import SelectorGroupChat
from autogen_agentchat.conditions import TextMentionTermination  , MaxMessageTermination
from dotenv import load_dotenv
from autogen_agentchat.base import TaskResult

# Load environment variables
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("Please set the OPENAI_API_KEY environment variable.")

# Initialize the OpenAI model client
openai_client = OpenAIChatCompletionClient(model="gpt-4o-mini", api_key=api_key)


DataAnalysisExpert = AssistantAgent(
    name='DataAnalysisExpert',
    description="An expert agent that solves problems using code execution.",
    model_client=openai_client,
    system_message='You are a data Analysis agent that is an expert in give insigne and Answer qustion by Understand given Data,' \
    'You will be working with code executor agent to execute code' \
    'You will be give a task and you should first install the depended library using Shell scipt  cmd ex: ```bash\npip install pandas matplotlib \n```' \
    'Then you should give the code in Python Block format so that it can be ran by code executor agent' \
    'You can provide Shell scipt as well if code fails due to missing libraries, make sure to use pip install command' \
    'You should only give a single code block and pass it to executor agent'\
    'You should give the corrected code in Python Block format if error is there' \
    'Once the code has been successfully executed and you have the results. You should explain the results in detail' \
    # 'Make sure each code has 3 test cases and the output of each test case is printed' \
    'if you have to save the file, save it with output.png or output.txt or output.gif' \
    'Once everything is done, you should explain the results and say "STOP" to stop the conversation'
)

docker = DockerCommandLineCodeExecutor(
    work_dir='tmp',
    timeout=120,
    # Add volume mapping to access your Excel files

    
    init_command="pip install pandas matplotlib"
)

code_executor_agent = CodeExecutorAgent(
    name='CodeExecutorAgent',
    description="An agent that executes code in a Docker container.",
    code_executor=docker,
)
human_agent = UserProxyAgent(
    name='HumanAgent',
    description="A human agent that interacts with the team. Ast only if you need guidance or clarification, Keep the conversation minimal with Human Agent.",
    input_func = input,
)

termination_condition = TextMentionTermination('STOP') or MaxMessageTermination(15)


team = SelectorGroupChat(
    participants=[DataAnalysisExpert, code_executor_agent,human_agent],
    termination_condition=termination_condition,
    model_client=openai_client,
    )

async def run_code_executor_agent():
    try:
        await docker.start()

        task = 'Analyze the given dataset provided in customers-1000.csv. create the mechine leaning model using given dataset' \

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

    finally:
        await docker.stop()

if __name__=='__main__':
    import asyncio
    asyncio.run(run_code_executor_agent())
    print("Code execution completed.")