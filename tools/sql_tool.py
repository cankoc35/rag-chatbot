from langchain_community.utilities import SQLDatabase
from langchain_community.tools.sql_database.tool import QuerySQLDataBaseTool, InfoSQLDatabaseTool
from config.config import DB_URI

def get_sql_tool():
    db = SQLDatabase.from_uri(DB_URI)
    raw_tool = QuerySQLDataBaseTool(db=db)

    def wrapped_query(query: str) -> str:
        result = raw_tool.run(query)
        return str(result)  

    return wrapped_query

def get_info_tool():
    db = SQLDatabase.from_uri(DB_URI)
    return InfoSQLDatabaseTool(db=db)
