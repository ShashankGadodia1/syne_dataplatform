import datetime
import json

from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.utils.dates import datetime
from airflow.utils.dates import timedelta

default_args = {
    'owner': 'swapnali',
    'depends_on_past': False,
    'start_date': datetime(2023, 11, 22),
    'email': ['swapnalibharambe@gmail.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5)
}

dag = DAG(
    'Manfest_file_all_models_dag',
    default_args=default_args,
    description='A dbt wrapper for airflow',
    schedule_interval=timedelta(days=1),
)

def load_manifest():
    local_filepath = "/usr/local/airflow/dbt/airflow_dbt_l3/target/manifest.json"
    with open(local_filepath) as f:
        data = json.load(f)

    return data

def make_dbt_task(node, dbt_verb):
    """Returns an Airflow operator either run and test an individual model"""
    DBT_DIR = "/usr/local/airflow/dags/dbt"
    GLOBAL_CLI_FLAGS = "--no-write-json"
    model = node.split(".")[-1]

    if dbt_verb == "build":
        dbt_task = BashOperator(
            task_id=node.split(".")[-1],
            bash_command=f"""
            cd /usr/local/airflow/dbt/airflow_dbt_l3 &&
            dbt {GLOBAL_CLI_FLAGS} {dbt_verb} --profiles-dir /usr/local/airflow/dbt/airflow_dbt_l3/dbt_profiles --target dev --models {model} 
            """,
            dag=dag,
        )

  #  elif dbt_verb == "test":
   #     node_test = node.replace("model", "test")
    #    dbt_task = BashOperator(
     #       task_id=node_test,
      #      bash_command=f"""
       #     cd /usr/local/airflow/dbt/airflow_dbt_l3 &&
        #    dbt {GLOBAL_CLI_FLAGS} {dbt_verb} --profiles-dir /usr/local/airflow/dbt/airflow_dbt_l3/dbt_profiles --target dev --models {model}
         #   """,
          #  dag=dag,
        #)

    return dbt_task

data = load_manifest()

dbt_tasks = {}
for node in data["nodes"].keys():
    if node.split(".")[0] == "model":
      #  node_test = node.replace("model", "test")

        dbt_tasks[node] = make_dbt_task(node, "build")
       # dbt_tasks[node_test] = make_dbt_task(node, "test")

for node in data["nodes"].keys():
    if node.split(".")[0] == "model":

        # Set dependency to run tests on a model after model runs finishes
       # node_test = node.replace("model", "test")
        #dbt_tasks[node] >> dbt_tasks[node_test]

        # Set all model -> model dependencies
        for upstream_node in data["nodes"][node]["depends_on"]["nodes"]:

            upstream_node_type = upstream_node.split(".")[0]
            if upstream_node_type == "model":
                dbt_tasks[upstream_node] >> dbt_tasks[node]