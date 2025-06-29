from fastapi import FastAPI
from models import QueryInput, ReportOptionsResponse, ChatResponse          #, SubReportOptionsResponse, FilterRequestResponse
from memory import get_session, update_session
from logic import classify_intent, get_available_reports, get_subreports_for
from report_engine import generate_report
from fastapi.middleware.cors import CORSMiddleware
from logic import call_llm_api
from h_r_flow import handle_report_flow
from nav_logic import nav_button
from filters_api import router as filters_router
from connection import router as connection_router
from get_r import router as show_report
from get_rep_mod import router as modify_report

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
    
    if user_input.button in ["reset_report", "reset_sub_report", "reset_sub_sub_report"]:
        return nav_button(user_input,session)

    intent = classify_intent(user_input.text, user_input.button,user_input.selections,user_input.columns)
    print(intent)
    if intent == "chat":
        session.stage = "chat"
        update_session(user_input.session_id, session)
        message=call_llm_api([{ "role": "user", "content": user_input.text }])
        print(message)
        return ChatResponse(response=message)
    elif intent == "report":
        if session.stage in ["start", "chat"] or user_input.button == "Report":
            session.stage = "report_selected"
            session.report_type = None
            session.subreport_type = None
            session.subsubreport_type=None
            session.selected_columns = []
            update_session(user_input.session_id, session)
            return ReportOptionsResponse(
                response="What type of report do you want?",
                options=get_available_reports(),
                stage="report"
            )
        return handle_report_flow(user_input, session)

    return ChatResponse(response="Could not detect intent. Please try again.")


app.include_router(filters_router,tags=["Filter"])
app.include_router(connection_router, prefix="/auth", tags=["Connection"])
app.include_router(show_report,tags=["Report"])
app.include_router(modify_report,tags=["Report"])