from fastapi import Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

security = HTTPBearer(auto_error=False)

def require_admin(creds: HTTPAuthorizationCredentials = Depends(security)):
    return {"role": "admin", "token": creds.credentials if creds else None}
