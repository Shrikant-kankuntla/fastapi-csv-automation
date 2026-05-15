```md
# FastAPI CSV Automation API

A Python project that demonstrates how to build a **REST API using FastAPI** with **CSV-based storage**, **CSV upload + processing (clean/transform)**, and **automation tasks** (reports, backups, validation, cleanup).

## Features

- **Employee CRUD API** (Create, Read, Update, Delete) backed by a CSV file
- **CSV upload endpoint** that:
  - removes duplicates
  - handles missing values
  - normalizes text/email
  - adds computed columns (bonus, total compensation)
- **Analytics endpoint** for salary statistics
- **Automation trigger** endpoint that:
  - generates department summary reports
  - creates timestamped backups
  - validates data quality (duplicates, negative salary, missing fields)
  - cleans up old generated files

## Tech Stack

- Python
- FastAPI
- Uvicorn
- Pandas
- Pydantic
- schedule (for background automation)

---

## Project Structure

```
.
├── main.py
├── models.py
├── csv_utils.py
├── automation.py
├── requirements.txt
├── data/
│   └── input.csv
└── reports/
    ├── report_*.csv
    └── backup_*.csv
```

> Note: `data/` and `reports/` may be created automatically at runtime. If you used `.gitignore` to ignore them, that's expected.

---

## Setup (Windows PowerShell)

### 1) Create and activate a virtual environment

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 2) Install dependencies

```powershell
pip install -r requirements.txt
```

### 3) Run the API

```powershell
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Open:

- API: http://localhost:8000
- Swagger Docs: http://localhost:8000/docs

---

## API Endpoints (Quick Guide)

### Health Check
- `GET /` → confirms server is running

### Employees CRUD
- `POST /employees` → create employee
- `GET /employees` → list employees (supports `?department=...`)
- `GET /employees/{emp_id}` → get employee by id
- `PUT /employees/{emp_id}` → update employee
- `DELETE /employees/{emp_id}` → delete employee

### CSV Upload + Processing
- `POST /upload-csv` → upload a CSV and generate `data/output.csv`

### Statistics
- `GET /stats/salary` → salary summary + department averages

### Automation
- `POST /automation/run` → runs report + backup + validation + cleanup

---

## Example Requests

### Create an employee

```bash
curl -X POST http://localhost:8000/employees ^
  -H "Content-Type: application/json" ^
  -d "{\"name\":\"Alice\",\"department\":\"Engineering\",\"salary\":90000,\"email\":\"alice@company.com\"}"
```

### List employees

```bash
curl http://localhost:8000/employees
```

### Filter employees by department

```bash
curl "http://localhost:8000/employees?department=Engineering"
```

### Trigger automation

```bash
curl -X POST http://localhost:8000/automation/run
```

---

## CSV Format

### Expected columns (recommended)

```csv
id,name,department,salary,email
1,Alice,Engineering,90000,alice@co.com
2,Bob,Marketing,75000,bob@co.com
```

### Upload behavior

When you upload a CSV (`POST /upload-csv`), the processor:
- trims/normalizes text
- converts email to lowercase
- fills missing salary with 0
- drops duplicates
- adds:
  - `bonus` = `salary * 0.10`
  - `total_compensation` = `salary + bonus`

---

## Notes / Troubleshooting

### Browser shows timeout for `0.0.0.0`
Use:

- http://localhost:8000
- http://127.0.0.1:8000

(`0.0.0.0` is for binding/listening, not for browsing.)

### Windows PowerShell execution policy (if venv activation fails)
If activation is blocked:

```powershell
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```

---

## Roadmap (Optional Improvements)

- Replace CSV storage with SQLite/PostgreSQL
- Add authentication (JWT / OAuth2)
- Add pagination + sorting
- Dockerize the API
- Add CI (GitHub Actions) + tests (pytest)

---

## License

MIT (or choose your preferred license)
```
