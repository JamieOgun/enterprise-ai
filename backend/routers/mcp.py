from fastmcp import FastMCP
from database import DatabaseConnection
import openai
from data import initial_mcp_instances

mcp = FastMCP("My Server")

DB = DatabaseConnection()
DB.connect() 

@mcp.tool
def generate_sql_query(query: str) -> dict:
    """Generate a SQL query based on the user's request and allowed tables"""
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
        request = mcp.get_http_request()
        instance_id = request.query_params.get("mcp_name")

        if not instance_id:
            return "Error: No instance_id found in request"
        
        mcp_instance = next((mcp for mcp in initial_mcp_instances if mcp["id"] == instance_id), None)
        
        if not mcp_instance:
            return "Error: MCP instance not found"
        
        allowed_tables = mcp_instance["allowedTables"]
        
        if DB.connection is None:
            DB.connect()
        return DB.build_schema_context(schemas=allowed_tables)  # Can return string directly
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

mcp_app = mcp.http_app()  # Add this line

if __name__ == "__main__":
    mcp.run()