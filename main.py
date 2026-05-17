from fastapi import FastAPI, HTTPException, UploadFile, File, Query
from typing import List, Optional 
import shutil
import os

from models import Employee, EmployeeUpdate, CSVResponse, DepartmentEnum
from csv_utils import (
    add_employee,
    get_all_employees,
    get_employee_by_id,
    update_employee,
    delete_employee,
    filter_by_department,
    get_salary_stats,
    process_uploaded_csv,
    ensure_data_dir,
)

app = FastAPI(
    title="Employee API",
    description="Basic CRUD API with CSV processing & automation",
    version="1.0.0",
)


@app.on_event("startup")
def startup():
    ensure_data_dir()
    print(" Data directory ready.")


@app.get("/")
def root():
    return {"message": "Employee API is running ", "docs": "/docs"}


@app.post("/employees", response_model=dict, status_code=201)
def create_employee(employee: Employee):
    result = add_employee(employee)
    return {"message": "Employee created", "data": result}


@app.get("/employees", response_model=List[dict])
def list_employees(
    department: Optional[str] = Query(None, description="Filter by department"),
    limit: int = Query(100, le=500),
):
    if department:
        return filter_by_department(department)
    return get_all_employees()[:limit]


@app.get("/employees/{emp_id}")
def read_employee(emp_id: int):
    emp = get_employee_by_id(emp_id)
    if not emp:
        raise HTTPException(status_code=404, detail="Employee not found")
    return emp


@app.put("/employees/{emp_id}")
def update_employee_endpoint(emp_id: int, updates: EmployeeUpdate):
    result = update_employee(emp_id, updates)
    if not result:
        raise HTTPException(status_code=404, detail="Employee not found")
    return {"message": "Employee updated", "data": result}


@app.delete("/employees/{emp_id}")
def delete_employee_endpoint(emp_id: int):
    success = delete_employee(emp_id)
    if not success:
        raise HTTPException(status_code=404, detail="Employee not found")
    return {"message": "Employee deleted"}


@app.post("/upload-csv", response_model=CSVResponse)
def upload_csv(file: UploadFile = File(...)):
    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="Only .csv files allowed")

    temp_path = f"data/temp_{file.filename}"
    with open(temp_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    result = process_uploaded_csv(temp_path)
    os.remove(temp_path)  

    return CSVResponse(
        message="CSV processed successfully",
        rows_processed=result["rows_processed"],
        file_path=result["file_path"],
    )


@app.get("/stats/salary")
def salary_statistics():
    return get_salary_stats()


@app.post("/automation/run")
def trigger_automation():
    from automation import run_automation_task
    result = run_automation_task()
    return {"message": "Automation triggered", "result": result}

from fastapi.responses import FileResponse  

@app.get("/download/csv")
def download_csv():
    file_path = "data/input.csv"
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="CSV file not found")
    return FileResponse(
        path=file_path,
        filename="employees.csv",
        media_type="text/csv"
    )
