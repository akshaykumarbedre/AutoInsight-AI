from agent import create_human_agent ,create_code_exuter_agent, create_data_analysis_agent
from teams.team_manager import TeamManager
from config import get_openai_client
from tool import create_docker_cmd_code_excuter
from autogen_agentchat.base import TaskResult
from autogen_agentchat.messages import TextMessage
from util import run_code_executor_agent


team = TeamManager()

docker= create_docker_cmd_code_excuter()
code_excuter_agent=create_code_exuter_agent(docker=docker)

data_analysis_expert = create_data_analysis_agent(openai_client=get_openai_client())
human_agent = create_human_agent(Input_funtion=input)

data_analysis_team=team.create_data_analysis_team(openai_client=get_openai_client(), 
                               DataAnalysisExpert=data_analysis_expert,
                                code_executor_agent=code_excuter_agent,
                                human_agent=human_agent)


task1 = run_code_executor_agent(team=data_analysis_team,
                                docker=docker,
                                file_name='data.txt',
                                task="display the data ")

task2 = run_code_executor_agent(team=data_analysis_team,
                                docker=docker,
                                file_name='None',
                                task="give me summary what we discuss ")

async def run_tasks():
    try:
        await task1
        await task2
    except Exception as e:
        print(f"An error occurred during task execution: {e}")


if __name__ == '__main__':
    import asyncio
    asyncio.run(run_tasks())
    print("Code execution completed.")