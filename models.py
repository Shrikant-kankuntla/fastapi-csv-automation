from pydantic import BaseModel
from typing import Optional
from enum import Enum


class Employee(BaseModel):
    id: Optional[int] = None
    name: str
    department: str
    salary: float
    email: str


class EmployeeUpdate(BaseModel):
    name: Optional[str] = None
    department: Optional[str] = None
    salary: Optional[float] = None
    email: Optional[str] = None


class DepartmentEnum(str, Enum):
    engineering = "Engineering"
    marketing = "Marketing"
    sales = "Sales"
    hr = "HR"
    finance = "Finance"


class CSVResponse(BaseModel):
    message: str
    rows_processed: int
    file_path: str