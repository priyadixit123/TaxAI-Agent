
from backend.salary_validator import validate_salary_data

sample_salary = {
    "employee_name": "Rahul Sharma",
    "month": "April 2026",
    "basic_salary": 60000,
    "hra": 20000,
    "other_allowance": 10000,
    "gross_salary": 90000,
    "tds": 5000,
    "net_salary": 85000,
}

result = validate_salary_data(sample_salary)
print(result)
