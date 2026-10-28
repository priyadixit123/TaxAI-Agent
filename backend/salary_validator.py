
def validate_salary_data(data: dict) -> dict:
    required_fields = [
        "employee_name", "month", "basic_salary", "hra",
        "other_allowance", "gross_salary", "tds", "net_salary"
    ]

    missing_fields = [
        field for field in required_fields
        if data.get(field) is None or data.get(field) == ""
    ]

    errors = []
    numeric_fields = [
        "basic_salary", "hra", "other_allowance",
        "gross_salary", "tds", "net_salary"
    ]

    for field in numeric_fields:
        value = data.get(field)

        if value is None:
            continue

        if isinstance(value, bool) or not isinstance(value, (int, float)):
            errors.append(f"{field} must be a number.")
        elif value < 0:
            errors.append(f"{field} cannot be negative.")

    if not errors:
        basic = data.get("basic_salary")
        hra = data.get("hra")
        allowance = data.get("other_allowance")
        gross = data.get("gross_salary")
        tds = data.get("tds")
        net = data.get("net_salary")

        if all(v is not None for v in [basic, hra, allowance, gross]):
            expected_gross = basic + hra + allowance

            if abs(expected_gross - gross) > 1:
                errors.append(
                    f"Gross salary mismatch: expected {expected_gross}, "
                    f"but received {gross}."
                )

        if all(v is not None for v in [gross, tds, net]):
            expected_net = gross - tds

            if abs(expected_net - net) > 1:
                errors.append(
                    f"Net salary mismatch: expected {expected_net}, "
                    f"but received {net}."
                )

    return {
        "is_valid": not missing_fields and not errors,
        "missing_fields": missing_fields,
        "errors": errors,
    }
