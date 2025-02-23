from __future__ import annotations

import sys

from common import print_hello
from snowflake.snowpark.session import Session
from common import copy_to_table
from schema import schemas
from config import configs


def hello_procedure(session: Session, name: str) -> str:
    return print_hello(name)


def test_procedure(session: Session) -> str:
    return "Test procedure"

def copy_to_table_proc(session: Session) -> str:
    copied_into_result, qid = copy_to_table(session=session, config_file=configs.employee_config, schema=schemas.emp_stg_schema)

def copy_to_emp_tgt_proc(session: Session) -> str:
    session.sql("EXECUTE IMMEDIATE FROM @dev_deployment/de_project_1/load_to_emp_tgt.sql").collect()

# For local debugging
# Beware you may need to type-convert arguments if you add input parameters
if __name__ == "__main__":
    # Create a local Snowpark session
    with Session.builder.config("local_testing", True).getOrCreate() as session:
        print(hello_procedure(session, *sys.argv[1:]))  # type: ignore
