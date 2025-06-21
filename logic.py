from config import REPORTS_METADATA
from ollama import Client
from typing import List,Optional

ollama_client = Client(host='http://localhost:11434')

def get_available_reports():
    return list(REPORTS_METADATA.keys())

def get_subreports_for(report_type):
    """
    Returns the first-level subreport titles (like 'Precontracts Phase') under a main report (like 'Procurement').
    """
    if isinstance(report_type, list):
        report_type = report_type[0]

    report_dict = REPORTS_METADATA.get(report_type, {})
    return list(report_dict.keys()) if isinstance(report_dict, dict) else []

def get_columns_for(topic: str, subreport: str, subsubreport: Optional[str] = None) -> List[str]:
    if subsubreport:
        return list(REPORTS_METADATA.get(topic, {}).get(subreport, {}).get(subsubreport, {}).get("columns", []))
    else:
        return list(REPORTS_METADATA.get(topic, {}).get(subreport, {}).get("columns", []))
    

def has_subsubreports(topic: str, subreport: str) -> bool:
    value = REPORTS_METADATA.get(topic, {}).get(subreport)
    return isinstance(value, dict) and any(isinstance(v, dict) for v in value.values())
def get_subsubreports(topic: str, subreport: str) -> List[str]:
    return list(REPORTS_METADATA.get(topic, {}).get(subreport, {}).keys())

def get_filter(topic:str,subreport: str, subsubreport:Optional[str]=None)-> List[str]:
    print(topic,subreport,subsubreport)
    if subsubreport:
        return list(REPORTS_METADATA.get(topic, {}).get(subreport, {}).get(subsubreport, {}).get("Filters", []))
    else:
        return list(REPORTS_METADATA.get(topic,{}).get(subreport,{}).get("Filters",[]))




def classify_intent(text=None, button=None,selections=None,columns=None):
    if selections or columns:
        return "report"
    if button:
        if button.lower() in ['report', 'viewall']:
            return button.lower()
    if text:
        prompt = (
            'Classify the intent of the following user message as one of: '
            '"need_report", "want_report", "general_info", "other".\n'
            f'Message: "{text}"\n'
            'Respond with only the intent label.'
        )
        messages = [
        {"role": "system", "content": "You are an intent classification assistant."},
        {"role": "user", "content": prompt}
    ]
        intent = call_llm_api(messages).lower()
        if intent in ("need_report", "want_report"):
            return "report"
        elif intent in ("ask_about_report", "general_info"):
            return "chat"
        else:
            return "chat"
    return "chat"


def call_llm_api(messages, model="llama3.1:8b"):
    
    try:
        response = ollama_client.chat(model=model, messages=messages)
        return response['message']['content'].strip()
    except Exception as e:
        return f"LLM Error: {str(e)}"
    
    
def get_final_reports(topic, subreport):
    return list(REPORTS_METADATA.get(topic, {}).get(subreport, {}).keys())
