from pydantic import BaseModel,Field
from typing import List,Optional,Dict,Union
from datetime import date

class ApiInput(BaseModel):
    pottoken: str
    jsession: str
class QueryInput(BaseModel):
    session_id: str
    #user_query: str
    text: Optional[str] = None
    button: Optional[str] = None
    selections: Optional[List[str]] = None
    columns: Optional[List[str]] = None
    Filters: Optional[List[str]] = None
    
class ReportOptionsResponse(BaseModel):
    response: str
    options: List[str]
    stage: Optional[str] = None


class SubReportOptionsResponse(BaseModel):
     response: str
     options: List[str]
     stage: Optional[str] = None


class FilterRequestResponse(BaseModel):
    response: str
    options: List[str]
    stage:Optional[str] = None

class ChatResponse(BaseModel):
    response: str

class SessionData(BaseModel):
    session_id: str
    stage: str="start"
    report_type: Optional[str] = None
    subreport_type: Optional[str] = None
    subsubreport_type:Optional[str] = None
    selected_columns:list[str] = []
    selected_Filters:list[str]=[]
    
class LoginPayload(BaseModel):
    username: str
    password: str
    clientcode: str
    potSeed: str
    
class get_report(BaseModel):
    pottoken: str
    jsession: str
    session_id: str
    fromDate: str
    toDate: str
    loginUser: Union[str, bool]
    projIds: List[int]
    status: Optional[int] = None

