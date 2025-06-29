import requests
from fastapi import APIRouter, HTTPException
from typing import List
from models import get_report
from tabulate import tabulate
from memory import get_session, update_session

router = APIRouter()

@router.post("/report/Procurement/modify")
def get_procurement_report(report: get_report):
    pottoken = report.pottoken
    jsession = report.jsession
    session=get_session("session-1200")
    selected_columns=session.selected_columns
    print(selected_columns)

    payload = {
        "toDate": report.toDate,
        "fromDate":report.fromDate,
        "loginUser": report.loginUser,
        "projIds": report.projIds,
        "status": report.status
    }
    print(payload)
    url = "https://dev.rajutech.com/app/procurement/getLatestPreContracts"
    custom_headers = {
        "Content-Type": "application/json;charset=UTF-8",
        "pottoken": pottoken,
        "Cookie": f"JSESSIONID={jsession}"
    }

    response = requests.post(url, headers=custom_headers, json=payload, verify=False)

    if response.status_code != 200:
        raise HTTPException(status_code=500, detail="Failed to fetch report.")

    raw_data = response.json()
    contracts = raw_data.get("preContractTOs", [])

    column_field_map = {
        "EPS Name": lambda item: item.get("epsName", ""),
        "Project Name": lambda item: item.get("projName", ""),
        "Pre-Contract Id": lambda item: item.get("code", ""),
        "Contract Type": lambda item: item.get("preContractType", ""),
        "Contract Description": lambda item: item.get("desc", ""),
        "Pre-Contract Stage": lambda item: (
            "Contract Signed" if item.get("contractStageStatus") == "Purchase Order" 
            else item.get("contractStageStatus", "")
        ),
        "Post Contract Status": lambda item: (
            "Open" if item.get("poStatus") == 1 else 
            "Close" if item.get("poStatus") == 0 else ""
        )
    }
    report_rows = []
    for item in contracts:
        row = {col: column_field_map[col](item) for col in selected_columns if col in column_field_map}
        report_rows.append(row)

        
    if report_rows:
        print("\n🧾 Report Table:")
        print(tabulate(report_rows, headers="keys", tablefmt="pretty"))
    else:
        print("⚠️ No report data available.")
    print("\n\n\n\n\n\n\n\n")

    return {
        "columns": list(report_rows[0].keys()) if report_rows else [],
        "data": report_rows
    }
