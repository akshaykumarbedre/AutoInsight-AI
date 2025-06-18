from autogen_agentchat.agents import AssistantAgent

def create_database_agent(model_client, db_tools):
    """Create database agent with SQL capabilities"""
    return AssistantAgent(
        "Database_enginer",
        model_client=model_client,
        tools=db_tools,
        system_message="Your task is convert the user query into SQL query and return Data, Respond with 'TERMINATE' if the task is completed",
        description="This agent handles database queries and data retrieval and convert the text into sql which have access to Database"
    )
