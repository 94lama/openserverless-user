#--kind python:default
#--web true

import json
from create import main as create
from delete import main as delete
from listuser import main as listuser

"""
args:
- action: ["listuser", "adduser", "deleteuser"]
- username
- email (only for adduser)
- password (only for adduser)
- options: {
    milvus,
    minio,
    mongo,
    postgres,
    redis
}
"""
def main(args):
    # Get action from path or query parameter
    action = args.get("action")
    path = args.get("__ow_path", "")
    
    # If no action in query params, extract from path
    if not action and path:
        # Remove leading slash and get the action
        action = path.lstrip("/")
        if "/" in action:
            action = action.split("/")[0]
    
    # Handle the case where action might contain the full path
    if action and "/" in action:
        # Extract just the action part from the path
        if "action=" in action:
            action = action.split("action=")[-1].split("&")[0]
        else:
            # If it's a path, extract the last part
            action = action.split("/")[-1]
    
    params = {}
    if action not in ["listuser", "adduser", "deleteuser"]: 
        params = {"error": f"Action not valid: {action}. Available actions: listuser, adduser, deleteuser. Path: {path}"}
    elif action == "listuser": 
        params = listuser()
    elif action == "adduser": 
        params = create(args)
    else: 
        params = delete(args)

    return {
        "statusCode": 200,
        "headers": {
            'Content-Type': 'application/json', 
        },
        "body": params
    }

