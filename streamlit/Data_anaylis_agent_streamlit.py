import streamlit as st
from agent import create_human_agent, create_code_exuter_agent, create_data_analysis_agent
from teams.team_manager import TeamManager
from config import get_openai_client
from tool import create_docker_cmd_code_excuter
from util.stream_data_anaylisi import run_code_executor_agent_streamlit
import asyncio
import os 

# Initialize components
team = TeamManager()
docker = create_docker_cmd_code_excuter()
code_excuter_agent = create_code_exuter_agent(docker=docker)
data_analysis_expert = create_data_analysis_agent(openai_client=get_openai_client())

def take_human_input(prompt):
    """Function to take human input using Streamlit dialog"""
    input_value = " Good to go  "
    return input_value


human_agent = create_human_agent(Input_funtion=lambda prompt: take_human_input(prompt))

data_analysis_team = team.create_data_analysis_team(
    openai_client=get_openai_client(),
    DataAnalysisExpert=data_analysis_expert,
    code_executor_agent=code_excuter_agent,
    human_agent=human_agent
)

# Streamlit app
st.title("AI-Powered Task Executor with Human in the Loop")

# File upload
uploaded_file = st.file_uploader("Upload a file for analysis", type=["txt", "csv", "json"],)
if uploaded_file:
    file_name = uploaded_file.name
    with open(os.path.join("tmp/",file_name), "wb") as f:
        f.write(uploaded_file.getbuffer())
    st.success(f"File '{file_name}' uploaded successfully!")

# Task input
task = st.text_input("Enter the task for the agent (e.g., 'display the data', 'give me a summary')")

# Task execution section
if st.button("Run Task"):
    if uploaded_file or task:
        try:
            # Create message containers for streaming output
            message_area = st.empty()
            progress_placeholder = st.empty()
            
            # Create and display progress bar
            progress_bar = progress_placeholder.progress(0)
            
            # Create a container for streaming messages
            message_container = st.container()
            
            # Run the task asynchronously with streaming
            async def run_task():
                message_container.write("Task started. Streaming output:")
                async_gen = run_code_executor_agent_streamlit(
                    team=data_analysis_team,
                    docker=docker,
                    file_name=file_name if uploaded_file else "None",
                    task=task
                )
                
                # Process the streamed output
                async for message_data in async_gen:
                    if message_data["type"] == "message":
                        with message_container:
                            st.markdown(f"**{message_data['source']}:** {message_data['content']}")
                    elif message_data["type"] == "task_result":
                        with message_container:
                            st.markdown(f"**Task completed:** {message_data['stop_reason']}")
                    elif message_data["type"] == "error":
                        with message_container:
                            st.error(message_data["message"])
                
                message_area.success("Task processing complete!")
                progress_placeholder.empty()
            
            # Run the async task
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            loop.run_until_complete(run_task())
            
        except Exception as e:
            st.error(f"An error occurred: {e}")
    else:
        st.warning("Please upload a file and enter a task before running.")

# Graph display section with expander
with st.expander("Show Graph", expanded=False):
    if os.path.exists("tmp/output.png"):
        st.image("tmp/output.png", caption="Generated Graph", use_column_width=True)
    else:
        st.warning("Graph image not found. Please generate a graph first.")