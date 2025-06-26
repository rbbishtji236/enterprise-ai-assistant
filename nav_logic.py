from memory import update_session
from logic import get_available_reports,get_subreports_for,get_subsubreports
from models import ReportOptionsResponse

def nav_button(user_input,session):

    if user_input.button == "reset_report":
        session.stage = "report_selected"
        session.report_type = None
        session.subreport_type = None
        session.subsubreport_type = None
        session.selected_columns = []
        update_session(user_input.session_id, session)
        return ReportOptionsResponse(
            response="What type of report do you want?",
            options=get_available_reports(),
            stage=session.stage
        )
    elif user_input.button == "reset_sub_report":
        session.stage = "subreport_selected"
        session.subreport_type = None
        session.subsubreport_type = None
        session.selected_columns = []
        update_session(user_input.session_id, session)
        return ReportOptionsResponse(
            response=f"What type of subreport do you want for '{session.report_type}'?",
            options=get_subreports_for(session.report_type),
            stage=session.stage
        )
    elif user_input.button == "reset_sub_sub_report":
        session.stage = "subsubreport_selected"
        session.subsubreport_type = None
        session.selected_columns = []
        update_session(user_input.session_id, session)
        return ReportOptionsResponse(
            response=f"Which section of '{session.subreport_type}' do you want to see?",
            options=get_subsubreports(session.report_type, session.subreport_type),
            stage=session.stage
        )
