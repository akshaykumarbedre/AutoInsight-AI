# %%
import asyncio
from config import get_openai_client, get_llm, load_environment
from database import DatabaseManager
from agent import create_database_agent, create_visualization_agent
from teams import TeamManager
from tool import (
    create_bar_chart, create_line_chart, create_histogram,
    create_scatter_plot, create_pie_chart
)
from util import stream_db_conversation, display_plot_result

# Global variables to store components
api_key = None
llm = None
model_client = None
db_manager = None
team_manager = None
db_agent = None
visualization_agent = None
db_team = None
visualization_team = None

def setup_application(db_uri: str = "sqlite:///ecommerce.db"):
    """Setup the application components"""
    global api_key, llm, model_client, db_manager, team_manager
    global db_agent, visualization_agent, db_team, visualization_team
    
    # Load configuration
    api_key = load_environment()
    llm = get_llm(api_key)
    model_client = get_openai_client()
    
    # Initialize components
    db_manager = DatabaseManager(db_uri)
    team_manager = TeamManager()
    
    # Setup database
    db_manager.connect(llm)
    db_tools = db_manager.get_tools()
    
    # Setup agents
    db_agent = create_database_agent(model_client, db_tools)
    
    plotting_tools = [
        create_line_chart, create_pie_chart, create_scatter_plot,
        create_histogram, create_bar_chart
    ]
    visualization_agent = create_visualization_agent(model_client, plotting_tools)
    
    # Setup teams
    db_team = team_manager.create_db_team(db_agent)
    visualization_team = team_manager.create_visualization_team(visualization_agent)

async def query_database(query: str):
    """Query database and return results"""
    print(f"🔍 Processing database query: {query}")
    
    stream_result = db_team.run_stream(task=query)
    result_data = None
    
    async for line in stream_db_conversation(stream_result):
        print(line)
        
            # Extract the actual result
    result_data = line.messages[-1].content.replace("TERMINATE", "").strip()
    
    return result_data

async def create_visualization(data: str, preferences: str = ""):
    """Create visualization from data"""
    print(f"📊 Creating visualization for data...")
    
    task = f"create the graph for given data {data}"
    if preferences:
        task += f", {preferences}"
    
    stream_result = visualization_team.run_stream(task=task)
    
    async for line in stream_db_conversation(stream_result):
        print(line)
    
            # Display the generated plot
    # display_plot_result(line.messages)
    
    return line

async def run_complete_workflow(query: str, visualization_preferences: str = ""):
    """Run complete workflow: query -> visualize"""
    # Step 1: Query database
    data = await query_database(query)
    
    if not data:
        print("❌ No data received from database query")
        return
    
    print(f"\n📋 Retrieved data: {data[:200]}...")
    
    # Step 2: Create visualization
    await create_visualization(data, visualization_preferences)
    
    # Step 3: Reset teams for next use
    await team_manager.reset_teams()

async def interactive_session():
    """Run interactive session with user"""
    print("🤖 Welcome to AutoInsight AI!")
    print("You can query your database and get visualizations.")
    print("Type 'quit' to exit.\n")
    
    while True:
        # Get database query
        query = input("📝 Enter your database query: ").strip()
        if query.lower() == 'quit':
            break
        
        # Get visualization preferences
        preferences = input("🎨 Visualization preferences (optional): ").strip()
        
        try:
            await run_complete_workflow(query, preferences)
        except Exception as e:
            print(f"❌ Error: {e}")
        
        print("\n" + "="*50 + "\n")

# Example usage and testing
async def main():
    """Main function for testing"""
    # Setup application
    setup_application()
    
    # Example 1: Simple query
    print("=== Example 1: Simple Query ===")
    await create_visualization(
        preferences="i want in red color",
        data="""- Laptop: $999.99
- Smartphone: $699.99
- Headphones: $199.99
- Coffee Maker: $149.99
- Organic Coffee: $24.99
- Wireless Mouse: $49.99
- Protein Bars: $19.99
- Tablet: $499.99
- Smart Watch: $299.99
- Blender: $89.99
- Yoga Mat: $39.99"""
    )
    
    # print("=== Example 1: Simple Query ===")
    # await run_complete_workflow(
    #     query="give me list of item nama and price",
    #     visualization_preferences="i want in red color"
    # )
    
    # print("=== Example 1: Simple Query ===")
    # await run_complete_workflow(
    #     query="give me list of item nama and price",
    #     visualization_preferences="i want in red color"
    # )
    
    # print("\n=== Example 2: Profit Analysis ===")
    # await run_complete_workflow(
    #     query="give me list of item nama and profit of each items",
    #     visualization_preferences="i want in deep pink color"
    # )


    
    # Uncomment to run interactive session
    # await interactive_session()

if __name__ == "__main__":
    asyncio.run(main())

