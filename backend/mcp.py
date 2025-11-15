from fastmcp import FastMCP
from database import DatabaseConnection
import openai

mcp = FastMCP("My Server")

DB = DatabaseConnection()
DB.connect() 

@mcp.tool
def generate_sql_query(query: str) -> dict:
    """Generate a SQL query based on the user's request"""
    response = openai.chat.completions.create(
        model="GPT5",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that generates SQL queries based on the user's request."},
            {"role": "user", "content": f"User request: {query}\n\nDatabase context: {DB.build_schema_context()}"}
        ]
    )
    sql_query = response.choices[0].message.content
    
    return {"sql_query": sql_query}


@mcp.tool
def get_database_context() -> str:  # Change to str
    """Get the database context"""
    try:
        if DB.connection is None:
            DB.connect()
        return DB.build_schema_context()  # Can return string directly
    except Exception as exc:
        return f"Error: {exc}"

@mcp.tool
def execute_query(query: str) -> dict:
    """Execute a query on the database"""
    try:
        if DB.connection is None:
            DB.connect()
        result = DB.execute_query(query)
        data = result.to_dict('records') if not result.empty else []
        return {"data": data}
    except Exception as exc:
        return {"error": str(exc)}

if __name__ == "__main__":
    mcp.run()