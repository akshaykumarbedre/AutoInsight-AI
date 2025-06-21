from sqlalchemy.engine import Result
from pydantic import BaseModel, Field
from typing import Any, Dict, Optional, Sequence, Type, Union
from langchain_core.callbacks import (
    AsyncCallbackManagerForToolRun,
    CallbackManagerForToolRun,
)
from config import get_llm
from langchain_community.utilities.sql_database import SQLDatabase
from langchain_community.agent_toolkits.sql.toolkit import SQLDatabaseToolkit
from langchain_community.utilities.sql_database import SQLDatabase
from langchain_core.tools import BaseTool
from pydantic import BaseModel, Field, root_validator, model_validator, ConfigDict

class BaseSQLDatabaseTool(BaseModel):
    """Base tool for interacting with a SQL database."""

    db: SQLDatabase = Field(exclude=True)

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
    )

class _QuerySQLDatabaseToolInput(BaseModel):
    query: str = Field(..., description="A detailed and correct SQL query.")

class QuerySQLDatabaseTool(BaseSQLDatabaseTool, BaseTool):
    """Tool for querying a SQL database.

    .. versionchanged:: 0.3.12

        Renamed from QuerySQLDataBaseTool to QuerySQLDatabaseTool.
        Legacy name still works for backwards compatibility.
    """

    name: str = "sql_db_query"
    description: str = """
    Execute a SQL query against the database and get back the result..
    If the query is not correct, an error message will be returned.
    If an error is returned, rewrite the query, check the query, and try again.
    """
    args_schema: Type[BaseModel] = _QuerySQLDatabaseToolInput

    def _run(
        self,
        query: str,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> Union[str, Sequence[Dict[str, Any]], Result]:
        """Execute the query, return the results or an error message."""

        if not query.strip().lower().startswith("select"):
            return "This tool can only be used to execute SELECT queries. not INSERT, UPDATE, DELETE, or other types of queries."
    
        return self.db.run_no_throw(query)
    


def get_sql_tools(url = "sqlite:///ecommerce.db"):
    db = SQLDatabase.from_uri(url)
    toolkit = SQLDatabaseToolkit(db=db, llm=get_llm())

    Custom_tool=QuerySQLDatabaseTool(db=db, description="Input to this tool is a detailed and correct SQL query, output is a result from the database. If the query is not correct, an error message will be returned. If an error is returned, rewrite the query, check the query, and try again. If you encounter an issue with Unknown column 'xxxx' in 'field list', use sql_db_schema to query the correct table fields.")


    """Get LangChain adapted tools from toolkit"""
    return [Custom_tool]+ toolkit.get_tools()[1:]
