import re
from db import (
    search_adverse_event_by_date,
    search_drug_by_pharmacologic_class,
    count_patient_reactions,
    search_drug_by_name,
)

TOOLS = {
    "search_adverse_event_by_date": {
        "func": search_adverse_event_by_date,
        "params": ["start_date", "end_date"]
    },
    "search_drug_by_pharmacologic_class": {
        "func": search_drug_by_pharmacologic_class,
        "params": ["pharm_class"]
    },
    "count_patient_reactions": {
        "func": count_patient_reactions,
        "params": ["pharm_class"]
    },
    "search_drug_by_name": {
        "func": search_drug_by_name,
        "params": ["drug_name"]
    }
}

async def run_agent(user_query: str) -> str:
    user_query = user_query.lower()

    # Example 1: Adverse effects of a drug
    m = re.search(r"adverse effects of ([a-z0-9\s]+)", user_query)
    if m:
        drug_name = m.group(1).strip()
        result = await TOOLS["search_drug_by_name"]["func"](drug_name=drug_name)
        return result

    # Example 2: Search adverse events between dates
    m = re.search(r"adverse events between (\d{4}-\d{2}-\d{2}) and (\d{4}-\d{2}-\d{2})", user_query)
    if m:
        start_date, end_date = m.group(1), m.group(2)
        result = await TOOLS["search_adverse_event_by_date"]["func"](start_date=start_date, end_date=end_date)
        return result

    # Example 3: Search drug by pharmacologic class
    m = re.search(r"drugs in pharmacologic class ([a-z\s]+)", user_query)
    if m:
        pharm_class = m.group(1).strip()
        result = await TOOLS["search_drug_by_pharmacologic_class"]["func"](pharm_class=pharm_class)
        return result

    # Example 4: Count patient reactions by pharmacologic class
    m = re.search(r"count patient reactions for ([a-z\s]+)", user_query)
    if m:
        pharm_class = m.group(1).strip()
        result = await TOOLS["count_patient_reactions"]["func"](pharm_class=pharm_class)
        return result

    return "Sorry, I could not understand your query. Please try asking about drug adverse effects, adverse events between dates, drugs by pharmacologic class, or patient reaction counts."
