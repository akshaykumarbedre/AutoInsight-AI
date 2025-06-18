from langchain_community.agent_toolkits.sql.toolkit import SQLDatabaseToolkit
from langchain_community.utilities.sql_database import SQLDatabase
from autogen_ext.tools.langchain import LangChainToolAdapter

class DatabaseManager:
    """Manages database connections and toolkit creation"""
    
    def __init__(self, db_uri: str = "sqlite:///ecommerce.db"):
        self.db_uri = db_uri
        self.db = None
        self.toolkit = None
        
    def connect(self, llm):
        """Connect to database and create toolkit"""
        self.db = SQLDatabase.from_uri(self.db_uri)
        self.toolkit = SQLDatabaseToolkit(db=self.db, llm=llm)
        
    def get_tools(self):
        """Get LangChain adapted tools from toolkit"""
        if not self.toolkit:
            raise ValueError("Database not connected. Call connect() first.")
        return [LangChainToolAdapter(tool) for tool in self.toolkit.get_tools()]
