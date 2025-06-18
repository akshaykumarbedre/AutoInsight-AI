import json
import ast
from IPython.display import Image, display
from autogen_agentchat.messages import ToolCallExecutionEvent

def display_plot_result(messages):
    """Display plot results from tool execution messages"""
    for message in messages.messages:
        try:
            if isinstance(message, ToolCallExecutionEvent):
           
                content_str = message.content[-1].content
                print(content_str)
                print(type(content_str))
                # Convert the string representation of dictionary to actual dictionary
                plot_result = ast.literal_eval(content_str)
                print(plot_result["plot_path"])
                
                # Display the image
                return plot_result['plot_path']
        except (ValueError, KeyError, IndexError, AttributeError) as e:
            print(f"An error occurred while processing the message: {e}")
            return None
