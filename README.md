# FastAPI CSV Automation 

A powerful FastAPI-based backend project for automating CSV processing, employee management, reporting, and scheduled data operations.

This project demonstrates practical backend development skills using FastAPI, Pandas, automation scripting, and REST APIs — ideal for learning backend engineering, automation workflows, and API development.

---

# 📌 Features

## Employee Management APIs
- Create employees
- Update employee records
- Delete employees
- Fetch employee details
- Department filtering
- Pagination support

---

## CSV Automation
- Upload CSV files
- Process employee datasets
- Remove duplicate records
- Clean missing values
- Normalize data
- Generate computed salary fields

---

## Reporting System
- Salary analytics
- Department-wise summaries
- Auto-generated reports
- Backup generation

---

## Scheduled Automation
- Automated validation
- Automatic backups
- Cleanup tasks
- Timed report generation

---

#  Tech Stack

| Technology | Usage |
|------------|------|
| Python | Core language |
| FastAPI | REST API framework |
| Pandas | CSV & data processing |
| Pydantic | Data validation |
| Uvicorn | ASGI server |
| Schedule | Task automation |

---

# Project Structure

```bash
fastapi-csv-automation/
│
├── main.py                # Main FastAPI application
├── automation.py          # Scheduled automation tasks
├── models.py              # Pydantic schemas
├── csv_utils.py           # CSV processing utilities
│
├── data/
│   └── employees.csv      # Employee dataset
│
├── reports/               # Generated reports & backups
│
├── requirements.txt
└── README.md
```

---

#  Installation

## 1️ Clone Repository

```bash
git clone https://github.com/Shrikant-kankuntla/fastapi-csv-automation.git
cd fastapi-csv-automation
```

---

## 2️ Create Virtual Environment

```bash
python -m venv venv
```

---

## 3️ Activate Virtual Environment

### Windows

```bash
venv\Scripts\activate
```

### Linux / Mac

```bash
source venv/bin/activate
```

---

## 4️ Install Dependencies

```bash
pip install -r requirements.txt
```

Or manually:

```bash
pip install fastapi uvicorn pandas schedule python-multipart
```

---

#  Running the Application

Start the FastAPI server:

```bash
uvicorn main:app --reload
```

Server runs on:

```bash
http://127.0.0.1:8000
```

---

#  API Documentation

FastAPI automatically provides Swagger UI.

## Swagger Docs

```bash
http://127.0.0.1:8000/docs
```

## ReDoc

```bash
http://127.0.0.1:8000/redoc
```

---

#  API Endpoints

# Base Endpoint

## GET /

Check API health status.

---

#  Employee APIs

## Create Employee

### POST `/employees`

### Example Request

```json
{
  "name": "John Doe",
  "department": "Engineering",
  "salary": 70000,
  "email": "john@example.com"
}
```

---

## Get All Employees

### GET `/employees`

### Query Parameters

| Parameter | Description |
|-----------|-------------|
| department | Filter employees |
| limit | Limit records |

### Example

```bash
/employees?department=Engineering&limit=5
```

---

## Get Employee By ID

### GET `/employees/{id}`

---

## Update Employee

### PUT `/employees/{id}`

---

## Delete Employee

### DELETE `/employees/{id}`

---

#  CSV APIs

## Upload CSV File

### POST `/upload-csv`

### Supported Features
- Duplicate cleanup
- Missing value handling
- Email normalization
- Salary transformation
- Bonus generation

---

## Download CSV

### GET `/download/csv`

Download processed employee data.

---

#  Salary Analytics

## GET `/stats/salary`

Returns:
- Average salary
- Highest salary
- Lowest salary
- Department statistics
- Salary distribution

---

# 🤖 Automation Tasks

Automation logic is implemented in:

```bash
automation.py
```

---

## Included Scheduled Tasks

| Task | Description |
|------|-------------|
| Report Generation | Generates analytics reports |
| Data Backup | Creates CSV backups |
| Validation | Detects invalid data |
| Cleanup | Removes old reports |

---

#  Run Automation Script

```bash
python automation.py
```

---

#  Sample CSV Format

```csv
id,name,department,salary,email
1,John Doe,Engineering,70000,john@example.com
2,Jane Smith,HR,50000,jane@example.com
```

---

# 🔍 Key Learning Concepts

This project demonstrates:

- REST API Development
- Backend Automation
- CSV Data Processing
- FastAPI Routing
- File Upload Handling
- Data Validation
- Scheduled Jobs
- API Documentation
- Clean Backend Architecture


#  Example Run

```bash
uvicorn main:app --reload
```

Then open:

```bash
http://127.0.0.1:8000/docs
```
