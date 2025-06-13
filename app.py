from fastapi import FastAPI
from models import QueryInput, ReportOptionsResponse, SubReportOptionsResponse, FilterRequestResponse, ChatResponse
from memory import get_session, update_session
from logic import classify_intent, get_available_reports, get_subreports_for, get_filters_for
from report_engine import generate_report

app = FastAPI()

@app.post("/ask", response_model=ReportOptionsResponse | SubReportOptionsResponse | FilterRequestResponse | ChatResponse)
def ask(user_input: QueryInput):
    session = get_session(user_input.session_id)
    

    intent = classify_intent(user_input.text, user_input.button)

    if intent == "report":
        if session.stage == "start":
            session.stage = "report_selected"
            update_session(user_input.session_id, session)
            return ReportOptionsResponse(
                prompt="Which reports do you want? Select from below:",
                options=get_available_reports()
            )
        elif session.stage == "report_selected":
            session.selected_reports = user_input.selections or []
            session.stage = "subreport_selected"
            update_session(user_input.session_id, session)
            return SubReportOptionsResponse(
                prompt="What type of subreport do you want for the selected reports?",
                options=get_subreports_for(session.selected_reports)
            )
        

    return ChatResponse(response="This is a general answer. (Plug in your LLM here.)")
