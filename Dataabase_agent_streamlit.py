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
import time
from PIL import Image

# Page configuration with modern styling
st.set_page_config(
    page_title="AutoInsight AI", 
    layout="wide",
    initial_sidebar_state="collapsed",
    page_icon="🤖"
)

# Custom CSS for modern UI
st.markdown("""
<style>
    /* Main container styling */
    .main-header {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        color: white;
        text-align: center;
    }
    
    /* Chat container styling */
    .chat-container {
        background: #f8f9ff;
        border-radius: 15px;
        padding: 1.5rem;
        margin-bottom: 1rem;
        border: 1px solid #e0e4e7;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    }
    
    /* Status indicators */
    .status-indicator {
        display: inline-block;
        width: 10px;
        height: 10px;
        border-radius: 50%;
        margin-right: 8px;
    }
    
    .status-active { background-color: #00ff00; }
    .status-processing { background-color: #ffa500; animation: pulse 1s infinite; }
    .status-idle { background-color: #cccccc; }
    
    @keyframes pulse {
        0% { opacity: 1; }
        50% { opacity: 0.5; }
        100% { opacity: 1; }
    }
    
    /* Message styling */
    .agent-message {
        background: white;
        border-radius: 10px;
        padding: 12px 16px;
        margin: 8px 0;
        border-left: 4px solid #667eea;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    }
    
    .tool-message {
        background: #f0f8ff;
        border-radius: 10px;
        padding: 12px 16px;
        margin: 8px 0;
        border-left: 4px solid #00bcd4;
    }
    
    .user-message {
        background: #e3f2fd;
        border-radius: 10px;
        padding: 12px 16px;
        margin: 8px 0;
        border-left: 4px solid #2196f3;
    }
    
    /* Button styling */
    .transfer-button {
        background: linear-gradient(45deg, #667eea, #764ba2);
        color: white;
        border: none;
        padding: 12px 24px;
        border-radius: 25px;
        font-weight: bold;
        cursor: pointer;
        transition: all 0.3s ease;
    }
    
    /* Progress indicators */
    .typing-indicator {
        display: inline-block;
        color: #666;
        font-style: italic;
    }
    
    .typing-indicator::after {
        content: '...';
        animation: typing 1s infinite;
    }
    
    @keyframes typing {
        0%, 33% { content: '.'; }
        34%, 66% { content: '..'; }
        67%, 100% { content: '...'; }
    }
</style>
""", unsafe_allow_html=True)

# Modern header
st.markdown("""
<div class="main-header">
    <h1>🤖 AutoInsight AI</h1>
    <p>Intelligent Data Analysis & Visualization Platform</p>
</div>
""", unsafe_allow_html=True)

# Initialize session state
if 'db_messages_history' not in st.session_state:
    st.session_state.db_messages_history = []
if 'viz_messages_history' not in st.session_state:
    st.session_state.viz_messages_history = []
if 'current_db_result' not in st.session_state:
    st.session_state.current_db_result = None
if 'processing_state' not in st.session_state:
    st.session_state.processing_state = {"db": "idle", "viz": "idle"}
if 'selected_query' not in st.session_state:
    st.session_state.selected_query = ""
if 'team' not in st.session_state:
    # Initialize agents
    st.session_state.team = TeamManager()
    st.session_state.database = DatabaseManager()
    st.session_state.database.connect()
    
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

# Enhanced message rendering function
def render_message(message_data, container, key_suffix=""):
    """Render a message with enhanced styling"""
    if message_data.get("type") == "text":
        emoji = message_data.get("emoji", "🤖")
        source = message_data.get("source", "Agent")
        content = message_data.get("content", "")
        
        container.markdown(f"""
        <div class="agent-message">
            <strong>{emoji} {source}</strong><br>
            {content}
        </div>
        """, unsafe_allow_html=True)
        
    elif message_data.get("type") == "user":
        content = message_data.get("content", "")
        
        container.markdown(f"""
        <div class="user-message">
            <strong>👤 You</strong><br>
            {content}
        </div>
        """, unsafe_allow_html=True)
        
    elif message_data.get("type") == "tool_request":
        tool_name = message_data.get("tool_name", "Unknown")
        arguments = message_data.get("arguments", {})
        
        container.markdown(f"""
        <div class="tool-message">
            <strong>🔧 Executing Tool: {tool_name}</strong><br>
            <small>Arguments: {str(arguments)[:100]}{'...' if len(str(arguments)) > 100 else ''}</small>
        </div>
        """, unsafe_allow_html=True)
        
    elif message_data.get("type") == "tool_result":
        tool_name = message_data.get("tool_name", "Unknown")
        content = message_data.get("content", "")
        
        container.markdown(f"""
        <div class="tool-message">
            <strong>✅ Tool Result: {tool_name}</strong><br>
            <small>{content}</small>
        </div>
        """, unsafe_allow_html=True)
        
    elif message_data.get("type") == "system":
        content = message_data.get("content", "")
        emoji = message_data.get("emoji", "ℹ️")
        
        container.markdown(f"""
        <div class="agent-message">
            <strong>{emoji} System</strong><br>
            {content}
        </div>
        """, unsafe_allow_html=True)
        
    elif message_data.get("type") == "visualization":
        container.markdown("""
        <div class="agent-message">
            <strong>📊 Visualization Complete</strong>
        </div>
        """, unsafe_allow_html=True)
        
        if "plot_path" in message_data:
            container.image(message_data["plot_path"], caption="Generated Visualization", use_column_width=True)
        
    else:
        # Fallback for other message types
        content = message_data.get("content", str(message_data))
        emoji = message_data.get("emoji", "ℹ️")
        
        container.markdown(f"""
        <div class="agent-message">
            <strong>{emoji} System</strong><br>
            {content}
        </div>
        """, unsafe_allow_html=True)

def display_chat_messages(messages, container_key):
    """Display all messages in chronological order"""
    for idx, message in enumerate(messages):
        render_message(message, st.container(), f"{container_key}_{idx}")

# Enhanced processing functions with real-time streaming
def process_database_query_sync(query, message_container, reset_team=True):
    """Synchronous database query processing with real-time UI updates"""
    st.session_state.processing_state["db"] = "processing"
    
    # Add processing indicator
    processing_msg = {
        "type": "system",
        "content": "🔍 Processing your query...",
        "emoji": "🔍"
    }
    st.session_state.db_messages_history.append(processing_msg)
    render_message(processing_msg, message_container)
    
    # Run the async function
    final_result = run_async(process_database_query_async(query, message_container, reset_team))
    
    st.session_state.processing_state["db"] = "idle"
    return final_result

async def process_database_query_async(query, message_container, reset_team=True):
    """Async database query processing with real-time streaming"""
    final_result = None
    
    if reset_team:
        await st.session_state.database_team.reset()
    
    db_result = st.session_state.database_team.run_stream(task=query)
    
    async for message in stream_db_conversation(db_result):
        if isinstance(message, dict):
            # Add to history and display immediately
            st.session_state.db_messages_history.append(message)
            render_message(message, message_container)
        else:
            # Handle the final result
            if hasattr(message, 'messages') and message.messages:
                final_result = message.messages[-1].content.replace("TERMINATE", '')
                
                # Add final result message
                result_msg = {
                    "type": "text",
                    "content": final_result,
                    "emoji": "✅",
                    "source": "Database Agent"
                }
                st.session_state.db_messages_history.append(result_msg)
                render_message(result_msg, message_container)
    
    return final_result

def process_visualization_query_sync(query, message_container):
    """Synchronous visualization processing with real-time UI updates"""
    st.session_state.processing_state["viz"] = "processing"
    
    # Add processing indicator
    processing_msg = {
        "type": "system",
        "content": "🎨 Creating visualization...",
        "emoji": "🎨"
    }
    st.session_state.viz_messages_history.append(processing_msg)
    render_message(processing_msg, message_container)
    
    # Run the async function
    run_async(process_visualization_query_async(query, message_container))
    
    st.session_state.processing_state["viz"] = "idle"

async def process_visualization_query_async(query, message_container):
    """Async visualization processing with real-time streaming"""
    viz_result = st.session_state.visualization_team.run_stream(task=query)
    
    async for message in stream_db_conversation(viz_result):
        if isinstance(message, dict):
            # Add to history and display immediately
            st.session_state.viz_messages_history.append(message)
            render_message(message, message_container)
        else:
            # Handle final visualization result
            if message:
                plot_path = display_plot_result(message)
                if plot_path:
                    # Add visualization result to history and display
                    viz_msg = {
                        "type": "visualization",
                        "content": "Generated visualization",
                        "plot_path": plot_path,
                        "emoji": "📊"
                    }
                    st.session_state.viz_messages_history.append(viz_msg)
                    render_message(viz_msg, message_container)

# Async handlers
def run_async(coro):
    """Run coroutine on the session event loop"""
    loop = st.session_state.event_loop
    return loop.run_until_complete(coro)

def handle_database_query(query):
    return run_async(process_database_query(query))

def handle_visualization_query(query):
    return run_async(process_visualization_query(query))

# Sidebar with enhanced information
with st.sidebar:
    st.markdown("### 🎯 How to Use")
    st.markdown("""
    1. **Database Query**: Ask questions about your data
    2. **Get Results**: Review the analysis results
    3. **Visualize**: Click to create visualizations
    4. **Refine**: Provide feedback to improve visualizations
    """)
    
    st.markdown("### 📊 Status")
    db_status = st.session_state.processing_state["db"]
    viz_status = st.session_state.processing_state["viz"]
    
    st.markdown(f"""
    - Database Agent: {'🟢 Active' if db_status == 'processing' else '⚪ Idle'}
    - Visualization Agent: {'🟢 Active' if viz_status == 'processing' else '⚪ Idle'}
    """)
    
    # Database Schema Section
    st.markdown("### 📁 Database Schema")
    
    # Customers Table
    with st.expander("📂 Customers", expanded=False):
        st.markdown("""
        **Fields:**
        - `customer_id` (INTEGER, PK) – Unique ID for each customer
        - `first_name` (TEXT, NOT NULL) – Customer's first name  
        - `last_name` (TEXT, NOT NULL) – Customer's last name
        - `email` (TEXT, Unique) – Customer's email
        - `phone` (TEXT) – Contact phone number
        - `registration_date` (DATE) – Date of registration
        - `city` (TEXT) – City of residence
        - `age` (INTEGER) – Customer's age
        """)
    
    # Orders Table
    with st.expander("📂 Orders", expanded=False):
        st.markdown("""
        **Fields:**
        - `order_id` (INTEGER, PK) – Unique ID for each order
        - `customer_id` (INTEGER, FK → Customers) – Who placed the order
        - `order_date` (DATE) – Date of order
        - `total_amount` (DECIMAL(10,2)) – Total order value
        - `status` (TEXT) – Status (e.g., "Fulfilled", "Pending")
        - `shipping_cost` (DECIMAL(6,2)) – Shipping fee applied
        """)
    
    # Order Items Table
    with st.expander("🧾 Order Items", expanded=False):
        st.markdown("""
        **Fields:**
        - `item_id` (INTEGER, PK) – Unique ID for order item
        - `order_id` (INTEGER, FK → Orders) – Linked order
        - `product_id` (INTEGER, FK → Products) – Purchased product
        - `quantity` (INTEGER) – Number of units ordered
        - `unit_price` (DECIMAL(10,2)) – Price per unit
        - `discount` (DECIMAL(5,2)) – Discount on item
        """)
    
    # Products Table
    with st.expander("📦 Products", expanded=False):
        st.markdown("""
        **Fields:**
        - `product_id` (INTEGER, PK) – Unique ID for product
        - `product_name` (TEXT, NOT NULL) – Name of product
        - `category` (TEXT) – Product category
        - `price` (DECIMAL(10,2)) – Product price
        - `stock_quantity` (INTEGER) – Number in stock
        - `supplier_id` (INTEGER) – Who supplied the product
        - `rating` (DECIMAL(3,2)) – Customer rating (1.0 - 5.0)
        """)
    
    # Suppliers Table
    with st.expander("🏢 Suppliers", expanded=False):
        st.markdown("""
        **Fields:**
        - `supplier_id` (INTEGER, PK) – Unique ID for supplier
        - `supplier_name` (TEXT, NOT NULL) – Name of the supplier
        - `contact_person` (TEXT) – Point of contact
        - `email` (TEXT) – Supplier email
        - `phone` (TEXT) – Phone number
        - `address` (TEXT) – Physical address
        - `country` (TEXT) – Country of origin
        - `performance_score` (DECIMAL(3,2)) – Score from 0.00 to 5.00
        """)
    
    # Query Tips
    with st.expander("💡 Query Tips", expanded=False):
        st.markdown("""
        **Sample Queries:**
        - "Show me top 10 customers by total orders"
        - "What are the most popular products?"
        - "Orders by month for this year"
        - "Customer demographics by city"
        - "Supplier performance comparison"
        
        **Abbreviations:**
        - PK = Primary Key
        - FK = Foreign Key
        """)
    
    if st.button("🔄 Reset Application", use_container_width=True):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()

# Enhanced dual-column layout
col1, col2 = st.columns([1, 1], gap="large")

# DATABASE CHAT COLUMN
with col1:
    st.markdown("""
    <div class="chat-container">
        <h3>🗄️ Database Agent</h3>
        <p>Ask questions about your data and get intelligent analysis</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Quick Start Suggestions
    st.markdown("**💡 Try these sample queries:**")
    
    # Sample queries
    sample_queries = [
        "Show me the top 10 customers by total order amount with their contact details",
        "What are the most popular products by quantity sold?",
        "Top order items by price in e-commmerse",
        "Show customer demographics breakdown by city and age groups",
        "Compare supplier performance scores and their delivery statistics"
    ]
    
    col1_1, col1_2 = st.columns(2)
    
    with col1_1:
        if st.button("👥 Show me the top 10 customers by total order amount with their contact details", 
                     use_container_width=True, help="Click to use this query"):
            st.session_state.selected_query = sample_queries[0]
            st.rerun()
        
        if st.button("📊 Top order items by price in e-commmers ", 
                     use_container_width=True, help="Click to use this query"):
            st.session_state.selected_query = sample_queries[2]
            st.rerun()
        
        if st.button("🏢 Compare supplier performance scores and their delivery statistics", 
                     use_container_width=True, help="Click to use this query"):
            st.session_state.selected_query = sample_queries[4]
            st.rerun()
    
    with col1_2:
        if st.button("⭐ What are the most popular products by quantity sold?", 
                     use_container_width=True, help="Click to use this query"):
            st.session_state.selected_query = sample_queries[1]
            st.rerun()
        
        if st.button("🌍 Show customer demographics breakdown by city and age groups", 
                     use_container_width=True, help="Click to use this query"):
            st.session_state.selected_query = sample_queries[3]
            st.rerun()
    
    # Show selected query if any
    if st.session_state.selected_query:
        st.markdown("**Selected Query:**")
        st.info(f"📝 {st.session_state.selected_query}")
        
        col_execute, col_clear = st.columns([3, 1])
        with col_execute:
            if st.button("🚀 Execute Query", use_container_width=True, type="primary"):
                # Add user message to history
                user_message = {
                    "type": "user",
                    "content": st.session_state.selected_query,
                    "emoji": "👤",
                    "timestamp": time.time()
                }
                st.session_state.db_messages_history.append(user_message)
                
                # Create a new container for streaming messages
                streaming_container = st.container()
                
                # Process query with real-time streaming
                final_result = process_database_query_sync(st.session_state.selected_query, streaming_container)
                st.session_state.current_db_result = final_result
                
                # Clear the selected query after execution
                st.session_state.selected_query = ""
                st.rerun()
        
        with col_clear:
            if st.button("❌ Clear", use_container_width=True):
                st.session_state.selected_query = ""
                st.rerun()
    
    st.markdown("---")
    
    # Create a container for messages that can be updated
    db_messages_container = st.container()
    
    # Display all database messages in order
    with db_messages_container:
        display_chat_messages(st.session_state.db_messages_history, "db")
    
    # Database input
    if db_input := st.chat_input("💬 Ask about your data...", key="db_input"):
        # Add user message to history
        user_message = {
            "type": "user",
            "content": db_input,
            "emoji": "👤",
            "timestamp": time.time()
        }
        st.session_state.db_messages_history.append(user_message)
        
        # Display user message immediately
        with db_messages_container:
            render_message(user_message, st.container())
        
        # Create a new container for streaming messages
        streaming_container = st.container()
        
        # Process query with real-time streaming
        final_result = process_database_query_sync(db_input, streaming_container)
        st.session_state.current_db_result = final_result
        
        st.rerun()  # Refresh to show all results
    
    # Enhanced visualization button
    if st.session_state.current_db_result is not None:
        st.markdown("---")
        if st.button("🎨 Create Visualization", use_container_width=True, type="primary"):
            # Add transfer message
            transfer_msg = {
                "type": "system",
                "content": "🔄 Transferring data to visualization agent...",
                "emoji": "🔄",
                "timestamp": time.time()
            }
            st.session_state.db_messages_history.append(transfer_msg)
            
            # Add to viz history
            viz_init_msg = {
                "type": "user",
                "content": f"Create a visualization for: {st.session_state.current_db_result[:200]}{'...' if len(st.session_state.current_db_result) > 200 else ''}",
                "emoji": "👤",
                "timestamp": time.time()
            }
            st.session_state.viz_messages_history.append(viz_init_msg)
            
            st.rerun()

# VISUALIZATION CHAT COLUMN
with col2:
    st.markdown("""
    <div class="chat-container">
        <h3>🎨 Visualization Agent</h3>
        <p>Create and refine data visualizations</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Create a container for visualization messages
    viz_messages_container = st.container()
    
    # Display all visualization messages in order
    with viz_messages_container:
        display_chat_messages(st.session_state.viz_messages_history, "viz")
    
    # Auto-trigger visualization if we have a new viz request
    if (st.session_state.viz_messages_history and 
        st.session_state.viz_messages_history[-1].get("type") == "user" and
        "Create a visualization for:" in st.session_state.viz_messages_history[-1].get("content", "")):
        
        # Create streaming container for visualization
        viz_streaming_container = st.container()
        
        # Process visualization with streaming
        process_visualization_query_sync(st.session_state.current_db_result, viz_streaming_container)
        
        st.rerun()
    
    # Visualization feedback input
    if st.session_state.viz_messages_history:
        if viz_input := st.chat_input("💬 Provide feedback on the visualization...", key="viz_input"):
            # Add user feedback to history
            feedback_msg = {
                "type": "user",
                "content": viz_input,
                "emoji": "👤",
                "timestamp": time.time()
            }
            # st.session_state.viz_messages_history.append(feedback_msg)
            
            # Display feedback immediately
            with viz_messages_container:
                render_message(feedback_msg, st.container())
            
            # Create streaming container for feedback processing
            feedback_streaming_container = st.container()
            
            # Process feedback with streaming
            combined_feedback = f"Original data: {st.session_state.current_db_result}\n\nFeedback: {viz_input}"
            process_visualization_query_sync(combined_feedback, feedback_streaming_container)
            
            st.rerun()
    else:
        st.info("💡 First, run a database query and click 'Create Visualization' to start.")

# Enhanced footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 20px;">
    <p>🤖 <strong>AutoInsight AI</strong> - Powered by Advanced AI Agents</p>
    <p><small>Transforming data into insights through intelligent conversation</small></p>
</div>
""", unsafe_allow_html=True)