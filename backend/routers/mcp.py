from fastmcp import FastMCP
from fastmcp.server.dependencies import get_http_request
from database import DatabaseConnection
import openai
from data import load_mcp_instances

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
def get_database_context() -> str:
    """Get the database context filtered by instance allowed tables"""
    try:
        request = get_http_request()
        
        # Extract instance_id from URL path
        path = request.url.path
        path_parts = path.strip("/").split("/")
        
        instance_id = None
        if "mcp" in path_parts:
            mcp_index = path_parts.index("mcp")
            if mcp_index + 1 < len(path_parts):
                instance_id = path_parts[mcp_index + 1]
        
        # Try query params (for MCP Inspector and direct API calls)
        if not instance_id:
            instance_id = request.query_params.get("id") or request.query_params.get("instance_id")
        
        # Try headers as fallback
        if not instance_id:
            instance_id = request.headers.get("X-MCP-Instance-ID")
        
        if not instance_id:
            return "Error: No instance_id found in request. Please provide instance_id in URL path (/llm/mcp/{instance_id}), query parameter (?id={instance_id}), or header (X-MCP-Instance-ID)."
        
        # Load fresh instances from file
        mcp_instances = load_mcp_instances()
        mcp_instance = next((mcp for mcp in mcp_instances if mcp["id"] == instance_id), None)
        
        if not mcp_instance:
            return f"Error: MCP instance not found for ID: {instance_id}"
        
        allowed_tables = mcp_instance.get("allowedTables", [])
        
        if DB.connection is None:
            DB.connect()
        
        # Build schema context filtered by allowed tables
        return DB.build_schema_context(schemas=allowed_tables)
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

mcp_app = mcp.http_app() 

if __name__ == "__main__":
    mcp.run()