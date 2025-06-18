import matplotlib.pyplot as plt
import os
from datetime import datetime
from typing import List, Union, Optional
# Add this at the top of your file, before any other imports
import matplotlib
matplotlib.use('Agg')  # Use the non-interactive Agg backend


def create_bar_chart(
    data: List[List[Union[str, int, float]]], 
    title: str = "Bar Chart", 
    color: str = 'skyblue', 
    xlabel: str = "Category", 
    ylabel: str = "Value"
) -> Union[dict]:
    """Create a bar chart from list data"""
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
    """Create a line chart from list data"""
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
    """Create a histogram from list data"""
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
    """Create a scatter plot from list data"""
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
    """Create a pie chart from list data"""
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
