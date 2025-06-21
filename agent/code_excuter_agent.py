from autogen_agentchat.agents import CodeExecutorAgent



def create_code_exuter_agent( docker):
    """Create database agent with SQL capabilities"""
    return CodeExecutorAgent(
    name='CodeExecutorAgent',
    description="An agent that executes code in a Docker container.",
    code_executor=docker,
)

