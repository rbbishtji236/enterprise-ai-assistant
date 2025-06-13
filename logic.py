from config import REPORTS_METADATA

def classify_intent(text=None, button=None):
    if button:
        if button.lower() in ['report', 'viewall']:
            return button.lower()
    if text:
        t = text.lower()
        if 'report' in t or 'data' in t or 'show me' in t:
            return 'report'
    return 'chat'

def get_available_reports():
    return list(REPORTS_METADATA.keys())

def get_subreports_for(reports):
    subreport_set = set()
    for r in reports:
        subreport_set.update(REPORTS_METADATA.get(r, {}).get("subreports", []))
    return list(subreport_set)

def get_filters_for(reports):
    filter_set = set()
    for r in reports:
        filter_set.update(REPORTS_METADATA.get(r, {}).get("filters", []))
    return list(filter_set)
