import schedule
import time
import threading
import datetime
import os
from csv_utils import (
    read_csv,
    write_csv,
    process_uploaded_csv,
    get_salary_stats,
)

REPORT_DIR = "reports"


def ensure_report_dir():
    os.makedirs(REPORT_DIR, exist_ok=True)


def generate_daily_report():
    ensure_report_dir()
    df = read_csv()

    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    report_path = os.path.join(REPORT_DIR, f"report_{timestamp}.csv")

    summary = df.groupby("department").agg(
        employee_count=("id", "count"),
        avg_salary=("salary", "mean"),
        total_salary=("salary", "sum"),
        max_salary=("salary", "max"),
        min_salary=("salary", "min"),
    ).reset_index()

    summary.to_csv(report_path, index=False)
    print(f" Report generated: {report_path}")
    return report_path


def backup_data():
    ensure_report_dir()
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = os.path.join(REPORT_DIR, f"backup_{timestamp}.csv")

    df = read_csv()
    df.to_csv(backup_path, index=False)
    print(f"💾 Backup created: {backup_path}")
    return backup_path


def validate_data():
    df = read_csv()
    issues = []

    duplicates = df[df.duplicated(subset=["email"])]
    if not duplicates.empty:
        issues.append(f"Found {len(duplicates)} duplicate emails")

    invalid_salary = df[df["salary"] < 0]
    if not invalid_salary.empty:
        issues.append(f"Found {len(invalid_salary)} negative salaries")

    missing = df.isnull().sum()
    for col, count in missing.items():
        if count > 0:
            issues.append(f"Column '{col}' has {count} missing values")

    if not issues:
        print(" Data validation passed — no issues found")
    else:
        print(f" Data validation issues: {issues}")

    return issues if issues else ["All good!"]


def cleanup_old_reports(days: int = 7):
    ensure_report_dir()
    now = datetime.datetime.now()
    cleaned = 0

    for filename in os.listdir(REPORT_DIR):
        filepath = os.path.join(REPORT_DIR, filename)
        file_time = datetime.datetime.fromtimestamp(os.path.getmtime(filepath))
        if (now - file_time).days > days:
            os.remove(filepath)
            cleaned += 1

    print(f" Cleaned {cleaned} old report(s)")
    return cleaned


def run_automation_task():
    report = generate_daily_report()
    backup = backup_data()
    issues = validate_data()
    cleaned = cleanup_old_reports()

    return {
        "report": report,
        "backup": backup,
        "validation": issues,
        "cleaned_files": cleaned,
    }


def run_scheduler():
    # Schedule tasks
    schedule.every(1).hours.do(generate_daily_report)
    schedule.every(6).hours.do(backup_data)
    schedule.every(30).minutes.do(validate_data)
    schedule.every().monday.do(lambda: cleanup_old_reports(days=7))

    print(" Scheduler started...")

    while True:
        schedule.run_pending()
        time.sleep(60)  


def start_scheduler():
    thread = threading.Thread(target=run_scheduler, daemon=True)
    thread.start()
    print("🚀 Background scheduler thread started")


# ---------- RUN DIRECTLY ----------
if __name__ == "__main__":
    print("Running automation tasks manually...")
    result = run_automation_task()
    print(result)
