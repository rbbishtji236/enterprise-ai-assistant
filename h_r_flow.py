from fastapi import FastAPI
from models import QueryInput, ReportOptionsResponse, ChatResponse, FilterRequestResponse
from memory import get_session, update_session
from logic import classify_intent, get_available_reports, get_subreports_for,has_subsubreports,get_subsubreports,get_columns_for,get_filter
from logic import call_llm_api

def handle_report_flow(user_input: QueryInput, session):
    if session.stage == "report_selected" and user_input.selections:
        session.report_type = user_input.selections[0] if isinstance(user_input.selections, list) else user_input.selections
        session.stage = "subreport_selected"
        update_session(user_input.session_id, session)
        return ReportOptionsResponse(
            response=f"What type of subreport do you want for '{session.report_type}'?",
            options=get_subreports_for(session.report_type),
            stage="subreports"
        )

    elif session.stage == "subreport_selected" and user_input.selections:
        session.subreport_type = user_input.selections[0] if isinstance(user_input.selections, list) else user_input.selections
        if has_subsubreports(session.report_type, session.subreport_type):
            session.stage = "subsubreport_selected"
            update_session(user_input.session_id, session)
            return ReportOptionsResponse(
                response=f"Which section of '{session.subreport_type}' do you want to see?",
                options=get_subsubreports(session.report_type, session.subreport_type),
                stage="subsubreports"
            )
        else:
            session.stage = "columns_selected"
            update_session(user_input.session_id, session)
            return ReportOptionsResponse(
                response=f"Which columns do you want in the '{session.subreport_type}' report?",
                options=get_columns_for(session.report_type, session.subreport_type),
                stage="columns1"
            )
    elif session.stage == "subsubreport_selected" and user_input.selections:
        session.subsubreport_type = user_input.selections[0] if isinstance(user_input.selections, list) else user_input.selections
        session.stage = "columns_selected"
        update_session(user_input.session_id, session)
        return ReportOptionsResponse(
            response=f"Which columns do you want in the '{session.subsubreport_type}' section?",
            options=get_columns_for(session.report_type, session.subreport_type, session.subsubreport_type),
            stage="columns"
        )

    elif session.stage == "columns_selected" and user_input.columns:
        session.selected_columns = user_input.columns
        print("before:",user_input.columns)
        print("save:",session.selected_columns)
        session.stage = "Filters"
        update_session(user_input.session_id, session)
        return FilterRequestResponse(response="ok then select all the filters.",
               options=get_filter(session.report_type, session.subreport_type, session.subsubreport_type),
               stage='Filters'                      
        
        )
    

    return ChatResponse(response="Still waiting for your input to proceed in report flow.")
