# %%
import asyncio
import sqlite3

import requests
from autogen_agentchat.agents import AssistantAgent, UserProxyAgent
from autogen_agentchat.conditions import TextMentionTermination
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.ui import Console
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_ext.tools.langchain import LangChainToolAdapter
from langchain_community.agent_toolkits.sql.toolkit import SQLDatabaseToolkit
from langchain_community.utilities.sql_database import SQLDatabase
from langchain_openai import ChatOpenAI
from typing import List, Sequence

from autogen_agentchat.agents import AssistantAgent, UserProxyAgent
from autogen_agentchat.conditions import MaxMessageTermination, TextMentionTermination
from autogen_agentchat.messages import BaseAgentEvent, BaseChatMessage



from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

from langchain_openai import ChatOpenAI

llm= ChatOpenAI(
    model="gpt-4.1-mini-2025-04-14",
    api_key=api_key,
)


from langchain_community.agent_toolkits.sql.toolkit import SQLDatabaseToolkit
from langchain_community.utilities.sql_database import SQLDatabase

db = SQLDatabase.from_uri("sqlite:///ecommerce.db")

toolkit = SQLDatabaseToolkit(db=db, llm=llm)

termination = TextMentionTermination("TERMINATE")

# Create the LangChain tool adapter for every tool in the toolkit.
tools = [LangChainToolAdapter(tool) for tool in toolkit.get_tools()]

# Create the chat completion client.
model_client = OpenAIChatCompletionClient(model="gpt-4o-mini")

# Create the assistant agent.
DB_agent = AssistantAgent(
    "Database_enginer",
    model_client=model_client,
    tools=tools,  # type: ignore
    model_client_stream=True,
    system_message="Your task is convert the user query into SQL query and return Data, Respond with 'TERMINATE' if the task is completed",
    description="This agent handles database queries and data retrieval and convert the text into sql which have access to Database"
)


import pandas as pd
import io
import base64
import matplotlib.pyplot as plt
import numpy as np
import os
from datetime import datetime
from typing import List, Tuple, Optional, Union

def create_bar_chart(
    data: List[List[Union[str, int, float]]], 
    title: str = "Bar Chart", 
    color: str = 'skyblue', 
    xlabel: str = "Category", 
    ylabel: str = "Value"
) -> Union[dict]:
    """
    Create a bar chart from list data
    
    Args:
        data: List of [category, value] pairs, e.g., [['A', 23], ['B', 45], ['C', 56]]
              This parameter is required and cannot be None or empty
        title: Title for the chart (default: "Bar Chart")
        color: Bar color (default: 'skyblue')
        xlabel: X-axis label (default: "Category")
        ylabel: Y-axis label (default: "Value")
    
    Returns:
        dict with plot path or error dict with 'error' key
    """
    try:
        if not data:
            return {"error": "Data parameter is required and cannot be empty. Expected format: [['category1', value1], ['category2', value2], ...]"}
        
        if not isinstance(data, list):
            return {"error": "Data must be a list of lists. Expected format: [['category1', value1], ['category2', value2], ...]"}
        
        for i, item in enumerate(data):
            if not isinstance(item, list) or len(item) != 2:
                return {"error": f"Data item at index {i} must be a list with exactly 2 elements [category, value]"}
        
        categories = [str(item[0]) for item in data]
        values = [float(item[1]) for item in data]
        
        plt.figure(figsize=(10, 6))
        plt.bar(categories, values, color=color)
        plt.title(title, fontsize=14, fontweight='bold')
        plt.xlabel(xlabel, fontsize=12)
        plt.ylabel(ylabel, fontsize=12)
        plt.grid(True, alpha=0.3, axis='y')
        plt.tight_layout()
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filepath = f"plots/bar_chart_{timestamp}.png"
        os.makedirs("plots", exist_ok=True)
        plt.savefig(filepath, dpi=300, bbox_inches='tight')
        plt.close()
        
        return {
            "status": "success",
            "plot_path": filepath,
            "absolute_path": os.path.abspath(filepath)
        }
    except Exception as e:
        plt.close()
        return {"error": f"Error creating bar chart: {str(e)}"}

def create_line_chart(
    data: List[List[Union[int, float]]], 
    title: str = "Line Chart", 
    color: str = 'blue', 
    xlabel: str = "X", 
    ylabel: str = "Y"
) -> Union[dict]:
    """
    Create a line chart from list data
    
    Args:
        data: List of [x, y] pairs, e.g., [[1, 10], [2, 20], [3, 15]]
              This parameter is required and cannot be None or empty
        title: Title for the chart (default: "Line Chart")
        color: Line color (default: 'blue')
        xlabel: X-axis label (default: "X")
        ylabel: Y-axis label (default: "Y")
    
    Returns:
        dict with plot path or error dict with 'error' key
    """
    try:
        if not data:
            return {"error": "Data parameter is required and cannot be empty. Expected format: [[x1, y1], [x2, y2], ...]"}
        
        if not isinstance(data, list):
            return {"error": "Data must be a list of lists. Expected format: [[x1, y1], [x2, y2], ...]"}
        
        for i, item in enumerate(data):
            if not isinstance(item, list) or len(item) != 2:
                return {"error": f"Data item at index {i} must be a list with exactly 2 numeric elements [x, y]"}
        
        x_values = [float(item[0]) for item in data]
        y_values = [float(item[1]) for item in data]
        
        plt.figure(figsize=(10, 6))
        plt.plot(x_values, y_values, marker='o', color=color, linewidth=2)
        plt.title(title, fontsize=14, fontweight='bold')
        plt.xlabel(xlabel, fontsize=12)
        plt.ylabel(ylabel, fontsize=12)
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filepath = f"plots/line_chart_{timestamp}.png"
        os.makedirs("plots", exist_ok=True)
        plt.savefig(filepath, dpi=300, bbox_inches='tight')
        plt.close()
        
        return {
            "status": "success",
            "plot_path": filepath,
            "absolute_path": os.path.abspath(filepath)
        }
    except Exception as e:
        plt.close()
        return {"error": f"Error creating line chart: {str(e)}"}

def create_histogram(
    data: List[Union[int, float]], 
    bins: int = 20, 
    title: str = "Histogram", 
    color: str = 'steelblue', 
    xlabel: str = "Values"
) -> Union[dict]:
    """
    Create a histogram from list data
    
    Args:
        data: List of numeric values, e.g., [1, 2, 3, 4, 5, 2, 3, 1]
              This parameter is required and cannot be None or empty
        bins: Number of bins for histogram (default: 20)
        title: Title for the chart (default: "Histogram")
        color: Bar color (default: 'steelblue')
        xlabel: X-axis label (default: "Values")
    
    Returns:
        dict with plot path or error dict with 'error' key
    """
    try:
        if not data:
            return {"error": "Data parameter is required and cannot be empty. Expected format: [value1, value2, value3, ...]"}
        
        if not isinstance(data, list):
            return {"error": "Data must be a list of numeric values. Expected format: [value1, value2, value3, ...]"}
        
        numeric_data = [float(x) for x in data]
        
        plt.figure(figsize=(10, 6))
        plt.hist(numeric_data, bins=bins, alpha=0.7, edgecolor='black', color=color)
        plt.title(title, fontsize=14, fontweight='bold')
        plt.xlabel(xlabel, fontsize=12)
        plt.ylabel("Frequency", fontsize=12)
        plt.grid(True, alpha=0.3, axis='y')
        plt.tight_layout()
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filepath = f"plots/histogram_{timestamp}.png"
        os.makedirs("plots", exist_ok=True)
        plt.savefig(filepath, dpi=300, bbox_inches='tight')
        plt.close()
        
        return {
            "status": "success",
            "plot_path": filepath,
            "absolute_path": os.path.abspath(filepath)
        }
    except Exception as e:
        plt.close()
        return {"error": f"Error creating histogram: {str(e)}"}

def create_scatter_plot(
    data: List[List[Union[int, float]]], 
    title: str = "Scatter Plot", 
    color: str = 'red', 
    xlabel: str = "X", 
    ylabel: str = "Y"
) -> Union[dict]:
    """
    Create a scatter plot from list data
    
    Args:
        data: List of [x, y] pairs, e.g., [[1, 2], [3, 4], [5, 6]]
              This parameter is required and cannot be None or empty
        title: Title for the chart (default: "Scatter Plot")
        color: Point color (default: 'red')
        xlabel: X-axis label (default: "X")
        ylabel: Y-axis label (default: "Y")
    
    Returns:
        dict with plot path or error dict with 'error' key
    """
    try:
        if not data:
            return {"error": "Data parameter is required and cannot be empty. Expected format: [[x1, y1], [x2, y2], ...]"}
        
        if not isinstance(data, list):
            return {"error": "Data must be a list of lists. Expected format: [[x1, y1], [x2, y2], ...]"}
        
        for i, item in enumerate(data):
            if not isinstance(item, list) or len(item) != 2:
                return {"error": f"Data item at index {i} must be a list with exactly 2 numeric elements [x, y]"}
        
        x_values = [float(item[0]) for item in data]
        y_values = [float(item[1]) for item in data]
        
        plt.figure(figsize=(10, 6))
        plt.scatter(x_values, y_values, alpha=0.7, color=color, s=50)
        plt.title(title, fontsize=14, fontweight='bold')
        plt.xlabel(xlabel, fontsize=12)
        plt.ylabel(ylabel, fontsize=12)
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filepath = f"plots/scatter_plot_{timestamp}.png"
        os.makedirs("plots", exist_ok=True)
        plt.savefig(filepath, dpi=300, bbox_inches='tight')
        plt.close()
        
        return {
            "status": "success",
            "plot_path": filepath,
            "absolute_path": os.path.abspath(filepath)
        }
    except Exception as e:
        plt.close()
        return {"error": f"Error creating scatter plot: {str(e)}"}

def create_pie_chart(
    data: List[List[Union[str, int, float]]], 
    title: str = "Pie Chart", 
    colors: Optional[List[str]] = None
) -> Union[dict]:
    """
    Create a pie chart from list data
    
    Args:
        data: List of [label, value] pairs, e.g., [['A', 25], ['B', 35], ['C', 20]]
              This parameter is required and cannot be None or empty
        title: Title for the chart (default: "Pie Chart")
        colors: List of colors for slices (default: None for automatic colors)
    
    Returns:
        dict with plot path or error dict with 'error' key
    """
    try:
        if not data:
            return {"error": "Data parameter is required and cannot be empty. Expected format: [['label1', value1], ['label2', value2], ...]"}
        
        if not isinstance(data, list):
            return {"error": "Data must be a list of lists. Expected format: [['label1', value1], ['label2', value2], ...]"}
        
        for i, item in enumerate(data):
            if not isinstance(item, list) or len(item) != 2:
                return {"error": f"Data item at index {i} must be a list with exactly 2 elements [label, value]"}
        
        labels = [str(item[0]) for item in data]
        values = [float(item[1]) for item in data]
        
        plt.figure(figsize=(8, 8))
        plt.pie(values, labels=labels, autopct='%1.1f%%', startangle=90, colors=colors)
        plt.title(title, fontsize=14, fontweight='bold')
        plt.axis('equal')
        plt.tight_layout()
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filepath = f"plots/pie_chart_{timestamp}.png"
        os.makedirs("plots", exist_ok=True)
        plt.savefig(filepath, dpi=300, bbox_inches='tight')
        plt.close()
        
        return {
            "status": "success",
            "plot_path": filepath,
            "absolute_path": os.path.abspath(filepath)
        }
    except Exception as e:
        plt.close()
        return {"error": f"Error creating pie chart: {str(e)}"}


# %%
tools=[create_line_chart , create_pie_chart , create_scatter_plot, create_histogram, create_bar_chart]
# Create the chat completion client.
model_client = OpenAIChatCompletionClient(model="gpt-4o-mini")

# Create the assistant agent.
Data_visualization = AssistantAgent(
    "Data_visualization",
    model_client=model_client,
    tools=tools,  # type: ignore
    system_message="You are a data visualization expert. Analyze the provided data and create the most suitable chart using one of these functions: create_line_chart, create_pie_chart, create_scatter_plot, create_histogram, or create_bar_chart. Choose the chart type that best represents the data patterns and relationships. After successfully creating the plot, respond with 'TERMINATE' to indicate task completion.",
    reflect_on_tool_use=False,
    description="This agent create the data visulization based given data"
)


# %%
db_team = RoundRobinGroupChat(
    
    [DB_agent],
    termination_condition=termination,
)

# %%
result=await Console(db_team.run_stream(task="i want to name items who pusrchase the mouse only  "))

# %%
print(result.messages[-1].content)


# %%
human_messag="i want to name items who pusrchase the mouse only "
result=await Console(db_team.run_stream(task=human_messag))



# %%
# button to reset to ask new question 
await db_team.reset()

# %%
nest_message=result.messages[-1].content.replace("TERMINATE"," ")

# %%
visualization = RoundRobinGroupChat(
    
    [Data_visualization],
    termination_condition=termination,
)

# %%
result=await Console(visualization.run_stream(task=f"create the graph for given data   {nest_message}, i want in red color "))

# %%
human_message="i wnat to color in deeppink"
result=await Console(visualization.run_stream(task=f"create the graph for given data   {nest_message}, review:{human_message}"))



