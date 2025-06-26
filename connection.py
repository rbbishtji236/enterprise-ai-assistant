import requests
from fastapi import APIRouter, HTTPException, Query
from typing import List
from models import LoginPayload

router = APIRouter()

@router.post("/connection_built", response_model=List[str])
def get_connection(payload:LoginPayload):
    
    session = requests.Session()
    
    login_payload= payload.dict()

    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    
    login_url = ""
    
    try:
        login_response = session.post(login_url, json=login_payload, headers=headers, verify=False)
        login_response.raise_for_status()
        data = login_response.json()

        pottoken = data.get("token")
        cookie = data.get("cookie")

        if not pottoken or not cookie:
            raise HTTPException(status_code=400, detail="Login response missing token or cookie.")

        jsession = cookie.split(';')[0].split('=')[1]
        return [pottoken, jsession]

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Login failed: {str(e)}")

    