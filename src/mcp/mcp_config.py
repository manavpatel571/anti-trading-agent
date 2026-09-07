import json
from pathlib import Path

def get_mcp_config():
    config_path = Path(__file__).parent.parent.parent / "mcp_servers" / "mcp_config.json"
    if config_path.exists():
        with open(config_path, "r") as f:
            return json.load(f)
    return {}
