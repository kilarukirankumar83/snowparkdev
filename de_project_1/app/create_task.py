from snowflake.core import Root
import snowflake.connector
from snowflake.core.task import StoredProcedureCall
from datetime import timedelta
import procedures
from snowflake.core.task.dagv1 import DAG, DAGOperation, DAGTask, CreateMode
from snowflake.snowpark.functions import udf
import os

connection = snowflake.connector.connect(user=os.environ.get("SNOWFLAKE_USER"), password=os.environ.get("SNOWFLAKE_PASSWORD"),\
                                         role=os.environ.get("SNOWFLAKE_ROLE"), database=os.environ.get("SNOWFLAKE_DATABASE"),\
                                         account=os.environ.get("SNOWFLAKE_ACCOUNT"),\
                                         warehouse=os.environ.get("SNOWFLAKE_WAREHOUSE"),\
                                        schema="PUBLIC")

# connection = snowflake.connector.connect()
root = Root(connection)

with DAG('dag_copy_emp',schedule=timedelta(days=1), warehouse="compute_wh", stage_location="@dev_deployment") as dag:
    dag_task_1 = DAGTask("copy_from_s3", StoredProcedureCall(procedures.copy_to_table_proc,\
                         stage_location="dev_deployment",\
                         packages=['snowflake-snowpark-python'], imports=['@dev_deployment/de_project_1/app.zip']),\
                         warehouse="compute_wh")
    
    dag_task_2 = DAGTask("copy_to_emp_tgt", StoredProcedureCall(procedures.copy_to_emp_tgt_proc,\
                         stage_location="dev_deployment",\
                         packages=['snowflake-snowpark-python'], imports=['@dev_deployment/de_project_1/app.zip']),\
                         warehouse="compute_wh")
    
    dag_task_1 >> dag_task_2

    schema = root.databases["demo_db"].schemas["public"]
    dag_op = DAGOperation(schema=schema)
    dag_op.deploy(dag, mode=CreateMode.or_replace)