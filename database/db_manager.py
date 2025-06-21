from tool.sql_tool_kit import get_sql_tools

from autogen_ext.tools.langchain import LangChainToolAdapter

class DatabaseManager:
    """Manages database connections and toolkit creation"""
    
    def __init__(self, db_uri: str = "sqlite:///ecommerce.db"):
        self.db_uri = db_uri
       
        self.toolkit = None
        
    def connect(self):
        """Connect to database and create toolkit"""
        
        self.toolkit = get_sql_tools( self.db_uri)
    
    def get_tools(self):
        """Get LangChain adapted tools from toolkit"""
        if not self.toolkit:
            raise ValueError("Database not connected. Call connect() first.")
        return [LangChainToolAdapter(tool) for tool in self.toolkit]
