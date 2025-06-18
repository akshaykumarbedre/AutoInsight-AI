"""
AutoInsight-AI main application
Integrates database analysis and visualization capabilities
"""

import asyncio
import os

from agent import create_database_agent, create_visualization_agent
from config import get_llm, get_openai_client
from database import DatabaseManager
from teams import TeamManager
from tool import (
    create_bar_chart, create_histogram, create_line_chart,
    create_pie_chart, create_scatter_plot
)
from util import display_plot_result, stream_db_conversation


def initialize_teams():
    """Initialize team managers and agents"""
    team = TeamManager()
    database = DatabaseManager()
    database.connect(get_llm())

    # Create database team with database agent
    database_team = team.create_db_team(
        create_database_agent(
            get_openai_client(),
            database.get_tools()
        )
    )

    # Create visualization team with visualization agent
    visualization_team = team.create_visualization_team(
        create_visualization_agent(
            get_openai_client(),
            [
                create_line_chart, create_pie_chart, create_scatter_plot,
                create_histogram, create_bar_chart
            ]
        )
    )
    
    return database_team, visualization_team


async def run_conversation(result):
    """Stream and print conversation results"""
    async for message in stream_db_conversation(result):
        print(message)


async def collect_results(result):
    """Collect streamed results and return the final content"""
    final_message = None
    async for message in stream_db_conversation(result):
        print(message)
        final_message = message
        
    return final_message.messages[-1].content.replace("TERMINATE", ' ')


async def collect_viz_messages(result):
    """Collect visualization messages for display"""
   
    async for message in stream_db_conversation(result):
        print(message)
       
        
    return message


async def main():
    """Main application flow"""
    # Initialize teams
    database_team, visualization_team = initialize_teams()
    
    # Example query - get top 7 products
    query_result = database_team.run_stream(task="i also want to top 3 product ")
    
    # Collect the results from the database query
    collected_data = await collect_results(query_result)
    
    # Pass the collected data to visualization team
    viz_result = visualization_team.run_stream(task=collected_data)
    viz_messages = await collect_viz_messages(viz_result)

    print(viz_messages)
    print(type(viz_messages))
    
    # Display the visualization
    plot_file_path = display_plot_result(viz_messages)
    
    # Show the path where the visualization is saved
    if plot_file_path:
        print(f"\nVisualization saved to: {plot_file_path}")
    else:
        print("\nNo visualization path returned. Check if the plot was displayed in a window.")


# Example of additional queries that can be uncommented as needed

# async def run_examples():
#     database_team, visualization_team = initialize_teams()
    
#     # Example 1: Get top 5 products by sales
#     result1 = database_team.run_stream(task="What are the top 5 products by sales")
#     await run_conversation(result1)
    
#     # Example 2: Direct visualization of sample data
#     sample_data = '''
#     1. Wireless Mouse - 7 units sold
#     2. Smart Watch - 4 units sold
#     3. Headphones - 2 units sold
#     4. Organic Coffee - 2 units sold
#     5. Tablet - 2 units sold
#     6. Blender - 2 units sold
#     7. Yoga Mat - 2 units sold
#     '''
#     result2 = visualization_team.run_stream(task=sample_data)
#     await collect_viz_messages(result2)



if __name__ == "__main__":
    asyncio.run(main())