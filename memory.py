
from models import SessionData

session_store = {}

def get_session(session_id: str) -> SessionData:
    if session_id not in session_store:
        session_store[session_id] = SessionData(stage="start")
    return session_store[session_id]

def update_session(session_id: str, session_data: SessionData):
    session_store[session_id] = session_data
