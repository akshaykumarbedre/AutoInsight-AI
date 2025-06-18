from autogen_agentchat.agents import AssistantAgent

def create_visualization_agent(model_client, plotting_tools):
    """Create visualization agent with plotting capabilities"""
    return AssistantAgent(
        "Data_visualization",
        model_client=model_client,
        tools=plotting_tools,
        system_message="You are a data visualization expert. Analyze the provided data and create the most suitable chart using one of these functions: create_line_chart, create_pie_chart, create_scatter_plot, create_histogram, or create_bar_chart. Choose the chart type that best represents the data patterns and relationships. After successfully creating the plot, respond with 'TERMINATE' to indicate task completion.",
        reflect_on_tool_use=False,
        description="This agent create the data visulization based given data"
    )
