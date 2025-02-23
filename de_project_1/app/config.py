
class configs:
    employee_config = {
        "Database_name": "DEMO_DB",
        "Schema_name": "Public",
        "Target_table": "EMPLOYEE",
        "Reject_table": "EMPLOYEE_REJECT",
        "target_columns": ["FIRST_NAME", "LAST_NAME", "EMAIL", "ADDRESS", "CITY", "DOJ"],
        "on_error": "CONTINUE",
        "Source_location": "@my_s3_stage/employee/",
        "Source_file_type": "csv"
    }
