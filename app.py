from fastapi import FastAPI
from models import QueryInput, ReportOptionsResponse, ChatResponse          #, SubReportOptionsResponse, FilterRequestResponse
from memory import get_session, update_session
from logic import classify_intent, get_available_reports, get_subreports_for
from report_engine import generate_report
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/ask", response_model=ReportOptionsResponse | ChatResponse)              #SubReportOptionsResponse | FilterRequestResponse |
def ask(user_input: QueryInput):
    session = get_session(user_input.session_id)
    print(user_input)
    if user_input.button=="Report":
        return ReportOptionsResponse(
                prompt="Which reports do you want? Select from below:",
                options=get_available_reports()
            )
    intent=""
    if user_input.selections :
        intent="report"
    else:
        intent = classify_intent(user_input.text, user_input.button)
       
    print(intent) 
        
    if intent == "report":
        if session.stage == "start":
            session.stage = "report_selected"
            update_session(user_input.session_id, session)
            return ReportOptionsResponse(
                prompt="Which reports do you want? Select from below:",
                options=get_available_reports()
            )
    
        # elif session.stage == "report_selected":
        #     # Receive report selections
        #     session.selected_reports = user_input.selections or []
        #     session.stage = "subreport_selected"
        #     update_session(user_input.session_id, session)
        #     # return SubReportOptionsResponse(
        #     #     prompt="What type of subreport do you want for the selected reports?",
        #     #     options=get_subreports_for(session.selected_reports)
        #     #)
        


    return ChatResponse(response="steps are not working properly.")
