from config import REPORTS_METADATA
from ollama import Client

ollama_client = Client(host='http://localhost:11434')

def get_available_reports():
    return list(REPORTS_METADATA.keys())

def get_subreports_for(reports):
    subreport_set = set()
    for r in reports:
        subreport_set.update(REPORTS_METADATA.get(r, {}).get("subreports", []))
    return list(subreport_set)


def classify_intent(text=None, button=None):
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
        intent = call_llm_api(prompt).lower()
        if intent in ("need_report", "want_report"):
            return "report"
        elif intent in ("ask_about_report", "general_info"):
            return "chat"
        else:
            return "chat"
    return "chat"


def call_llm_api(prompt, model="llama3.1:8b"):
    messages = [
        {"role": "system", "content": "You are an intent classification assistant."},
        {"role": "user", "content": prompt}
    ]
    try:
        response = ollama_client.chat(model=model, messages=messages)
        return response['message']['content'].strip()
    except Exception as e:
        return f"LLM Error: {str(e)}"
