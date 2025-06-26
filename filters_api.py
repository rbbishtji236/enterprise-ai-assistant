import requests
from fastapi import APIRouter, HTTPException, Query
from typing import List
from models import ApiInput

router = APIRouter()


@router.get("/filters/project-name", response_model=List[str])
def get_project_names(tokens:ApiInput):
    pottoken=tokens.pottoken
    jsession=tokens.jsession
    url = ""
    payload = {"status": 1}
    custom_headers = {
    "Content-Type": "application/json;charset=UTF-8",
    "pottoken": pottoken,
    "Cookie": f"JSESSIONID={jsession}"
    }

    response = requests.post(url, headers=custom_headers, json=payload, verify=False)
    data={}
    if response.status_code != 200:
        raise HTTPException(status_code=500, detail="Failed to fetch projects.")
    if response.status_code == 200:
        print("✅ Success:", response.status_code)
        data=response.json()
    else:
        print("❌ Failed:", response.status_code)
        print(response.text)
        
    leaf_projects = [] 
    if not data.get("epsProjs"):
        raise HTTPException(status_code=404, detail="No projects found.")  
        
    def find_leaf_projects(node, parent_name=None):
        children = node.get("childProjs", [])
        
        if not children:
            leaf_projects.append({
                "projName": node.get("projName"),
                "projId": node.get("projId"),
                "parentName": parent_name
            })
        else:
            for child in children:
                find_leaf_projects(child, node.get("projName"))
                
    # def find_leaf_projects_iterative(epsProjs):
    # stack = [(proj, None) for proj in epsProjs]  # (node, parent_name)
    # while stack:
    #     node, parent_name = stack.pop()
    #     children = node.get("childProjs", [])
    #     if not children:
    #         leaf_projects.append({
    #             "projName": node.get("projName"),
    #             "projId": node.get("projId"),
    #             "parentName": parent_name
    #         })
    #     else:
    #         for child in children:
    #             stack.append((child, node.get("projName")))

    for proj in data.get("epsProjs", []):
        find_leaf_projects(proj)
        
    for project in leaf_projects:
        print(f"Project: {project['projName']}, ID: {project['projId']}, Parent: {project['parentName']}")
        
        
    print(f"\nTotal leaf projects: {len(leaf_projects)}")
    
    return {"projects": leaf_projects}