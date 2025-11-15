from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List
from data import load_mcp_instances, save_mcp_instances

router = APIRouter()

BASE_URL = "https://enterprise-ai.onrender.com"

# Pydantic models for request/response
class MCPInstance(BaseModel):
    id: str
    name: str
    description: str
    url: str
    allowedTables: List[str]

@router.get("/")
def read_root():
    return {"message": "Hello, World!"}

@router.get("/mcp", response_model=List[MCPInstance])
def get_all_mcp_instances():
    """Get all MCP instances"""
    return load_mcp_instances()

@router.get("/mcp/{instance_id}", response_model=MCPInstance)
def get_mcp_instance(instance_id: str):
    """Get a specific MCP instance by ID"""
    instances = load_mcp_instances()
    instance = next((mcp for mcp in instances if mcp["id"] == instance_id), None)
    
    if not instance:
        raise HTTPException(status_code=404, detail="MCP instance not found")
    
    return instance

@router.delete("/mcp/{instance_id}", status_code=204)
def delete_mcp_instance(instance_id: str):
    """Delete an MCP instance"""
    instances = load_mcp_instances()
    instance_index = next((i for i, mcp in enumerate(instances) if mcp["id"] == instance_id), None)
    
    if instance_index is None:
        raise HTTPException(status_code=404, detail="MCP instance not found")
    
    instances.pop(instance_index)
    save_mcp_instances(instances)
    
    return None

@router.get("/llm/mcp")
def get_mcp():
    return {"mcp_url": f"{BASE_URL}/llm/mcp/"}
