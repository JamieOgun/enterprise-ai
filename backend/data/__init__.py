import json
from pathlib import Path
from typing import List, Dict, Any

# Load MCP instances from JSON file
_data_dir = Path(__file__).parent
_mcp_json_path = _data_dir / "mcp.json"

def load_mcp_instances() -> List[Dict[str, Any]]:
    """Load MCP instances from JSON file"""
    with open(_mcp_json_path, "r") as f:
        return json.load(f)

def save_mcp_instances(instances: List[Dict[str, Any]]) -> None:
    """Save MCP instances to JSON file"""
    with open(_mcp_json_path, "w") as f:
        json.dump(instances, f, indent=2)

# Load initial instances
initial_mcp_instances = load_mcp_instances()

__all__ = ["initial_mcp_instances", "load_mcp_instances", "save_mcp_instances"]
