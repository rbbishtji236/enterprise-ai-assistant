from pydantic import BaseModel,Field
from typing import List,Optional,Dict

class QueryInput(BaseModel):
    session_id: str
    #user_query: str
    text: Optional[str] = None
    button: Optional[str] = None
    selections: Optional[List[str]] = None
    
class ReportOptionsResponse(BaseModel):
    response: str
    options: List[str]

class SubReportOptionsResponse(BaseModel):
     response: str
     options: List[str]

# class FilterRequestResponse(BaseModel):
#     prompt: str
#     filters: List[str]

class ChatResponse(BaseModel):
    response: str

class SessionData(BaseModel):
    session_id: str
    stage: str="start"
    report_type: Optional[str] = None
    subreport_type: Optional[str] = None
    selected_columns:list[str] = []
