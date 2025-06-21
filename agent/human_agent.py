from autogen_agentchat.agents import UserProxyAgent

def create_human_agent(Input_funtion):
    """Create database agent with SQL capabilities"""
    return  UserProxyAgent( 
    name='HumanAgent',
    description="A human agent that interacts with the team. Ast only if you need guidance or clarification, Keep the conversation minimal with Human Agent.",
    input_func = Input_funtion,)
