from snowflake.core import Root
import snowflake.connector
from snowflake.core.task import Task, StoredProcedureCall
from datetime import timedelta
import procedures
from snowflake.core.task.dagv1 import DAG, DAGOperation, DAGTask, CreateMode, DAGTaskBranch
from snowflake.snowpark.session import Session
from snowflake.snowpark.functions import udf
import functions
import os

connection = snowflake.connector.connect(user=os.environ.get("SNOWFLAKE_USER"), password=os.environ.get("SNOWFLAKE_PASSWORD"),\
                                         role=os.environ.get("SNOWFLAKE_ROLE"), database=os.environ.get("SNOWFLAKE_DATABASE"),\
                                         account=os.environ.get("SNOWFLAKE_ACCOUNT"),\
                                         warehouse=os.environ.get("SNOWFLAKE_WAREHOUSE"),\
                                        schema="PUBLIC")
print("Connection established")
print(connection)

root = Root(connection)

print(root)

my_task = Task('my_task', StoredProcedureCall(procedures.hello_procedure, stage_location='dev_deployment'),\
 warehouse='compute_wh', schedule=timedelta(hours=1))

tasks = root.databases["demo_db"].schemas["public"].tasks

#tasks.create(my_task)

def task_condition_branch(session: Session) -> str:
    return "my_test_task3"

with DAG('my_dag',schedule=timedelta(days=1), warehouse="compute_wh", stage_location="@dev_deployment") as dag:
    dag_task_1 = DAGTask("my_hello_task", StoredProcedureCall(procedures.hello_procedure, args=["Kiran"], 
                         stage_location="dev_deployment",\
                         packages=['snowflake-snowpark-python'], imports=['@dev_deployment/first_snowpark/app.zip']),\
                         warehouse="compute_wh")
    
    dag_task_2 = DAGTask("my_test_task", StoredProcedureCall(procedures.test_procedure,\
                         stage_location='dev_deployment',\
                         packages=['snowflake-snowpark-python'], imports=['@dev_deployment/first_snowpark/app.zip']),\
                         warehouse="compute_wh")
    
    dag_task_3 = DAGTask("my_test_task3", StoredProcedureCall(procedures.hello_procedure, args=["Kiran"], 
                         stage_location="dev_deployment",\
                         packages=['snowflake-snowpark-python'], imports=['@dev_deployment/first_snowpark/app.zip']),\
                         warehouse="compute_wh")
    
    dag_task_4 = DAGTask("my_test_task4", StoredProcedureCall(procedures.test_procedure,\
                         stage_location='dev_deployment',\
                         packages=['snowflake-snowpark-python'], imports=['@dev_deployment/first_snowpark/app.zip']),\
                         warehouse="compute_wh")
    
    dag_task_1 >> dag_task_2 >> [dag_task_3, dag_task_4]

    schema = root.databases["demo_db"].schemas["public"]

    dag_op = DAGOperation(schema=schema)

    dag_op.deploy(dag, mode=CreateMode.or_replace)

with DAG('my_dag_task_branch',schedule=timedelta(days=1), warehouse="compute_wh", stage_location="@dev_deployment",\
          use_func_return_value=True, packages=["snowflake-snowpark-python"]) as dag_branch:
    dag_task_1 = DAGTask("my_hello_task", StoredProcedureCall(procedures.test_procedure,\
                         stage_location="dev_deployment",\
                         packages=['snowflake-snowpark-python'], imports=['@dev_deployment/first_snowpark/app.zip']),\
                         warehouse="compute_wh")
    
    dag_task_2 = DAGTask("my_test_task", StoredProcedureCall(procedures.test_procedure,\
                         stage_location='dev_deployment',\
                         packages=['snowflake-snowpark-python'], imports=['@dev_deployment/first_snowpark/app.zip']),\
                         warehouse="compute_wh")
    
    dag_task_3 = DAGTask("my_test_task3", StoredProcedureCall(procedures.test_procedure,\
                         stage_location="dev_deployment",\
                         packages=['snowflake-snowpark-python'], imports=['@dev_deployment/first_snowpark/app.zip']),\
                         warehouse="compute_wh")
    
    dag_task_4 = DAGTask("my_test_task4", StoredProcedureCall(procedures.test_procedure,\
                         stage_location='dev_deployment',\
                         packages=['snowflake-snowpark-python'], imports=['@dev_deployment/first_snowpark/app.zip']),\
                         warehouse="compute_wh")
    
    dag_task_branch = DAGTaskBranch("task_branch", task_condition_branch, warehouse="compute_wh")
    
    dag_task_1 >> dag_task_2 >> dag_task_branch

    dag_task_branch >> [dag_task_3, dag_task_4]

    schema = root.databases["demo_db"].schemas["public"]

    dag_op = DAGOperation(schema=schema)

    dag_op.deploy(dag_branch, mode=CreateMode.or_replace)


