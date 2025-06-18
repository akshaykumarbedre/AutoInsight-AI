import streamlit as st
from teams import TeamManager
from agent import create_database_agent, create_visualization_agent
from database import DatabaseManager
from config import get_openai_client, load_environment, get_llm
from tool import (
    create_bar_chart, create_line_chart, create_histogram,
    create_scatter_plot, create_pie_chart
)
from util import stream_db_conversation, display_plot_result
import asyncio
import json
from PIL import Image
from autogen_agentchat.messages import ToolCallExecutionEvent

# Page configuration
st.set_page_config(page_title="AutoInsight AI", layout="wide")
st.title("AutoInsight AI")

# Initialize session state to store conversation state
if 'db_messages_history' not in st.session_state:
    st.session_state.db_messages_history = []
if 'viz_messages_history' not in st.session_state:
    st.session_state.viz_messages_history = []
if 'current_db_result' not in st.session_state:
    st.session_state.current_db_result = None
if 'team' not in st.session_state:
    # Initialize agents
    st.session_state.team = TeamManager()
    st.session_state.database = DatabaseManager()
    st.session_state.database.connect(get_llm())
    
    st.session_state.database_team = st.session_state.team.create_db_team(
        create_database_agent(
            get_openai_client(),
            st.session_state.database.get_tools()
        )
    )
    
    st.session_state.visualization_team = st.session_state.team.create_visualization_team(
        create_visualization_agent(
            get_openai_client(),
            [
                create_line_chart, create_pie_chart, create_scatter_plot,
                create_histogram, create_bar_chart
            ]
        )
    )
if "event_loop" not in st.session_state:
    st.session_state.event_loop = asyncio.new_event_loop()
    asyncio.set_event_loop(st.session_state.event_loop)


# Helper function to determine message type and avatar
def get_message_avatar(message):
    message_text = str(message)
    
    # Tool call messages
    if "calling tool(s)" in message_text:
        return "🔧", f"Tool Call"
    elif "Tool(s) executed" in message_text:
        return "✅", f"Tool Execution"
    elif "ToolCallSummaryMessage" in message_text:
        return "ℹ️", f"Tool Summary"
    # Agent messages
    elif "Database_enginer" in message_text or "Database_engineer" in message_text:
        return "💬", "Database_engineer"
    elif "Visualization_engineer" in message_text:
        return "💬", "Visualization_engineer"
    # Default for other assistant messages
    else:
        return "🤖", "Assistant"

# Process database query in a single event loop
async def process_database_query(query, reset_team=True):
    messages = []
    final_result = None
    
    # Reset the team if requested
    if reset_team:
        await st.session_state.database_team.reset()
    
    # Run the database query
    db_result = st.session_state.database_team.run_stream(task=query)
    
    # Process and display messages
    async for message in stream_db_conversation(db_result):
        message_text = str(message)
        
        # Skip certain message types
        if "TextMessage" in message_text:
            continue
            
        # Determine avatar and role
        avatar, role = get_message_avatar(message)
        
        # Display message
        with st.chat_message(role, avatar=avatar):
            st.markdown(message_text)
        
        # Store message
        message_data = {
            "role": role,
            "avatar": avatar,
            "content": message_text
        }
        st.session_state.db_messages_history.append(message_data)
        messages.append(message)
    
    # Extract final result from last message
    if messages:

        final_result = message.messages[-1].content.replace("TERMINATE", '')
    
    return final_result

# Process visualization query in a single event loop
async def process_visualization_query(query):
   
    # Run the visualization query
    viz_result = st.session_state.visualization_team.run_stream(task=query)
    
    # Process and display messages
    async for message in stream_db_conversation(viz_result):
        message_text = str(message)
        
        # Skip certain message types
        if "TextMessage" in message_text:
            continue
            
        # Determine avatar and role
        avatar, role = get_message_avatar(message)
        
        # Display message
        with st.chat_message(role, avatar=avatar):
            st.markdown(message_text)
        
        # Store message
        message_data = {
            "role": role,
            "avatar": avatar,
            "content": message_text
        }
        st.session_state.viz_messages_history.append(message_data)
       
    
    # Process visualization result
    if message:
        plot_path = display_plot_result(message)
        if plot_path:
            with st.chat_message("Visualization", avatar="📊"):
                st.image(plot_path, caption="Generated Visualization")
            
            # Add to history
            st.session_state.viz_messages_history.append({
                "role": "Visualization",
                "avatar": "📊",
                "content": "Generated visualization",
                "plot_path": plot_path
            })

# Main async handler for database queries
import asyncio

# def handle_database_query(query):
#     try:
#         loop = asyncio.get_running_loop()
#     except RuntimeError:
#         # No current loop in this thread, so create one
#         loop = asyncio.new_event_loop()
#         asyncio.set_event_loop(loop)
    
#     return loop.run_until_complete(process_database_query(query))



# # Main async handler for visualization queries
# def handle_visualization_query(query):
#     try:
#         loop = asyncio.get_running_loop()
#     except RuntimeError:
#         loop = asyncio.new_event_loop()
#         asyncio.set_event_loop(loop)
    
#     return loop.run_until_complete(process_visualization_query(query))

def run_async(coro):
    """
    Run *coro* on the single event loop stored in st.session_state.
    Blocks until it finishes and returns the result.
    """
    loop = st.session_state.event_loop
    return loop.run_until_complete(coro)

def handle_database_query(query):
    return run_async(process_database_query(query))

def handle_visualization_query(query):
    return run_async(process_visualization_query(query))


# Sidebar with app information
with st.sidebar:
    st.header("About AutoInsight AI")
    st.write("""
    This application uses AI agents to help you analyze data and create visualizations.
    
    **How to use:**
    1. Enter a database query in the left chat
    2. Provide feedback in the same chat
    3. Click "Visualize Data" when ready
    4. Provide visualization feedback in the right chat
    """)
    
    if st.button("Reset Application"):
        # Reset all state
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()

# Create two-column layout for the dual chat interface
col1, col2 = st.columns(2)

# DATABASE CHAT COLUMN
with col1:
    st.header("Database Agent")
    
    # Display chat history for database with appropriate avatars
    for message in st.session_state.db_messages_history:
        with st.chat_message(message["role"], avatar=message.get("avatar", None)):
            st.markdown(message["content"])
    
    # Database query input
    if db_input := st.chat_input("Enter your database query or feedback", key="db_input_field"):
        # Add user message to history
        st.session_state.db_messages_history.append({"role": "user", "avatar": "💬", "content": db_input})
        
        # Display the user message
        with st.chat_message("user", avatar="💬"):
            st.markdown(db_input)
        
        with st.spinner("Database agent processing..."):
            # Process the query in a single event loop
            final_result = handle_database_query(db_input)
            
            # Store the result for visualization
            st.session_state.current_db_result = final_result
    
    # Visualize button (only enabled after database results are available)
    if st.session_state.current_db_result is not None:
        if st.button("Visualize Data"):
            # Add a message to the database chat about sending to visualization
            st.session_state.db_messages_history.append({
                "role": "system", 
                "avatar": "🔄",
                "content": "Sending data to visualization agent..."
            })
            
            # Display the system message
            with st.chat_message("system", avatar="🔄"):
                st.markdown("Sending data to visualization agent...")
            
            # Add the initial message to visualization history
            st.session_state.viz_messages_history.append({
                "role": "user", 
                "avatar": "💬",
                "content": f"Create a visualization for this data: {st.session_state.current_db_result}"
            })
            
            # Display the message in visualization chat
            with col2:
                with st.chat_message("user", avatar="💬"):
                    st.markdown(f"Create a visualization for this data: {st.session_state.current_db_result}")
            
            # Process with visualization agent in a single event loop
            with col2:
                handle_visualization_query(st.session_state.current_db_result)
            
            # Force rerun to update the UI
            st.rerun()

# VISUALIZATION CHAT COLUMN
with col2:
    st.header("Visualization Agent")
    
    # Display chat history for visualization with appropriate avatars
    for message in st.session_state.viz_messages_history:
        with st.chat_message(message["role"], avatar=message.get("avatar", None)):
            # Check if this is a message with a plot path
            if "plot_path" in message:
                st.markdown(message["content"])
                st.image(message["plot_path"], caption="Visualization")
            else:
                st.markdown(message["content"])
    
    # Visualization feedback input (only enabled if visualization history exists)
    if st.session_state.viz_messages_history:
        if viz_input := st.chat_input("Enter your visualization feedback", key="viz_input_field"):
            # Add user message to history
            st.session_state.viz_messages_history.append({
                "role": "user", 
                "avatar": "💬",
                "content": viz_input
            })
            
            # Display the user message
            with st.chat_message("user", avatar="💬"):
                st.markdown(viz_input)
            
            with st.spinner("Visualization agent processing..."):
                # Combine the feedback with original data
                combined_feedback = f"Original data: {st.session_state.current_db_result}\n\nFeedback: {viz_input}"
                
                # Process the visualization feedback in a single event loop
                handle_visualization_query(combined_feedback)
    else:
        st.info("Run a database query first, then click 'Visualize Data' to generate a visualization.")

# Footer
st.markdown("---")
st.caption("AutoInsight AI - Data Analysis and Visualization")