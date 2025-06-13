from pydantic import BaseModel,Field
from typing import List,Optional,Dict

class QueryInput(BaseModel):
    session_id: str
    text: Optional[str] = None
    button: Optional[str] = None
    selections: Optional[List[str]] = None
    
class ReportOptionsResponse(BaseModel):
    prompt: str
    options: List[str]

class SubReportOptionsResponse(BaseModel):
    prompt: str
    options: List[str]

class FilterRequestResponse(BaseModel):
    prompt: str
    filters: List[str]

class ChatResponse(BaseModel):
    response: str

class SessionData(BaseModel):
    stage: str
    selected_reports: List[str] = Field(default_factory=list)
    selected_subreports: List[str] = Field(default_factory=list)
    filters: Dict[str, str] = Field(default_factory=dict)

