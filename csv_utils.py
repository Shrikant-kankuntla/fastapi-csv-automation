import pandas as pd
import os
from typing import List, Optional
from models import Employee

DATA_DIR = "data"
INPUT_FILE = os.path.join(DATA_DIR, "input.csv")
OUTPUT_FILE = os.path.join(DATA_DIR, "output.csv")


# ---------- Ensure data directory exists ----------
def ensure_data_dir():
    os.makedirs(DATA_DIR, exist_ok=True)
    if not os.path.exists(INPUT_FILE):
        df = pd.DataFrame(columns=["id", "name", "department", "salary", "email"])
        df.to_csv(INPUT_FILE, index=False)


# ---------- Read all records ----------
def read_csv() -> pd.DataFrame:
    ensure_data_dir()
    return pd.read_csv(INPUT_FILE)


# ---------- Write DataFrame to CSV ----------
def write_csv(df: pd.DataFrame, path: str = INPUT_FILE):
    df.to_csv(path, index=False)


# ---------- Get next ID ----------
def get_next_id() -> int:
    df = read_csv()
    if df.empty:
        return 1
    return int(df["id"].max()) + 1


# ---------- CREATE ----------
def add_employee(employee: Employee) -> dict:
    df = read_csv()
    new_id = get_next_id()
    new_row = {
        "id": new_id,
        "name": employee.name,
        "department": employee.department,
        "salary": employee.salary,
        "email": employee.email,
    }
    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
    write_csv(df)
    return new_row


# ---------- READ ALL ----------
def get_all_employees() -> List[dict]:
    df = read_csv()
    return df.to_dict(orient="records")


# ---------- READ ONE ----------
def get_employee_by_id(emp_id: int) -> Optional[dict]:
    df = read_csv()
    match = df[df["id"] == emp_id]
    if match.empty:
        return None
    return match.iloc[0].to_dict()


# ---------- UPDATE ----------
def update_employee(emp_id: int, updates: EmployeeUpdate) -> Optional[dict]:
    df = read_csv()
    idx = df.index[df["id"] == emp_id]
    if idx.empty:
        return None

    for key, value in updates.model_dump(exclude_unset=True).items():
        df.at[idx[0], key] = value

    write_csv(df)
    return df.loc[idx[0]].to_dict()


# ---------- DELETE ----------
def delete_employee(emp_id: int) -> bool:
    df = read_csv()
    idx = df.index[df["id"] == emp_id]
    if idx.empty:
        return False
    df = df.drop(idx)
    write_csv(df)
    return True


# ---------- FILTER by department ----------
def filter_by_department(dept: str) -> List[dict]:
    df = read_csv()
    filtered = df[df["department"].str.lower() == dept.lower()]
    return filtered.to_dict(orient="records")


# ---------- STATISTICS ----------
def get_salary_stats() -> dict:
    df = read_csv()
    if df.empty:
        return {"message": "No data available"}
    stats = df["salary"].describe().to_dict()
    stats["by_department"] = df.groupby("department")["salary"].mean().to_dict()
    return stats


# ---------- PROCESS uploaded CSV ----------
def process_uploaded_csv(source_path: str, dest_path: str = OUTPUT_FILE) -> dict:
    """Read, clean, transform, and save a CSV file."""
    df = pd.read_csv(source_path)

    # --- Data Cleaning ---
    df.drop_duplicates(inplace=True)
    df.dropna(subset=["name", "email"], inplace=True)
    df["salary"] = df["salary"].fillna(0)
    df["name"] = df["name"].str.strip().str.title()
    df["department"] = df["department"].str.strip().str.title()
    df["email"] = df["email"].str.strip().str.lower()

    # --- Transformation: Add bonus column ---
    df["bonus"] = df["salary"] * 0.10
    df["total_compensation"] = df["salary"] + df["bonus"]

    # --- Save ---
    write_csv(df, dest_path)

    return {
        "rows_processed": len(df),
        "columns": list(df.columns),
        "file_path": dest_path,
    }