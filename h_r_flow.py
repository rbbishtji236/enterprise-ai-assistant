from fastapi import FastAPI
from models import QueryInput, ReportOptionsResponse, ChatResponse ,SubReportOptionsResponse            #, FilterRequestResponse
from memory import get_session, update_session
from logic import classify_intent, get_available_reports, get_subreports_for
from logic import call_llm_api

def handle_report_flow(user_input: QueryInput, session):
    if session.stage == "report_selected" and user_input.selections:
        session.report_type = user_input.selections[0] if isinstance(user_input.selections, list) else user_input.selections
        session.stage = "subreport_selected"
        update_session(user_input.session_id, session)
        return ReportOptionsResponse(
            response=f"What type of subreport do you want for '{session.report_type}'?",
            options=get_subreports_for(session.report_type)
        )

    # 3. Subreport selected
    elif session.stage == "subreport_selected" and user_input.selections:
        session.subreport_type = user_input.selections[0] if isinstance(user_input.selections, list) else user_input.selections
        session.stage = "awaiting_columns"
        update_session(user_input.session_id, session)
        return ReportOptionsResponse(
            response=f"Which columns do you want in the '{session.subreport_type}' report?",
            options=["rohit","bisht"]
            #options=get_columns(session.report_type, session.subreport_type)
        )

    # 4. Columns selected
    elif session.stage == "awaiting_columns" and user_input.selections:
        session.selected_columns = user_input.selections
        session.stage = "ready_to_generate"
        update_session(user_input.session_id, session)
        return ChatResponse(response="Thanks! Generating your report now...")#, columns=session.selected_columns)

    return ChatResponse(response="Still waiting for your input to proceed in report flow.")
