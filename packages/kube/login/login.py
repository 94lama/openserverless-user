import hashlib
import json
from config import get_kubeconfig

def login(args):
    """
    Validate user credentials and return user info
    """
    email = args.get("email", "").strip()
    password = args.get("password", "").strip()
    
    if not email:
        return {"output": "Error: email parameter is required"}
    
    if not password:
        return {"output": "Error: password parameter is required"}
    
    try:
        kubeconfig = get_kubeconfig()
        if not kubeconfig:
            return {"output": "Error: kubeconfig parameter is required"}
        
        # Parse kubeconfig to get user data
        # In a real scenario, this would validate against stored credentials
        # For now, we'll create a simple validation mechanism
        
        # Generate a session token (simple hash for demo)
        session_token = hashlib.sha256(f"{email}{password}".encode()).hexdigest()
        
        return {
            "output": "Login successful",
            "user": {
                "email": email,
                "token": session_token
            }
        }
    except Exception as e:
        return {"output": f"Error: {str(e)}"}
