import datetime
import json
import yaml

from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.utils.dates import datetime
from airflow.utils.dates import timedelta

dag_name="Manfest_file_model_1_2";


def load_manifest():
    local_filepath = "/usr/local/airflow/dbt/airflow_dbt_l3/target/manifest.json"
    with open(local_filepath) as f:
        data = json.load(f)

    return data
    
def load_config_yaml():
    local_yaml_filpath = "/usr/local/airflow/dbt/airflow_dbt_l3/dbtconfig/config.yaml"
    with open(local_yaml_filpath) as f:
        # use safe_load instead load
        dataMap = yaml.safe_load(f)
    print(dataMap)
    return dataMap
    
def get_dag_properties(dataMap):
    dag_properties=[]
    for k, v in dataMap["airflow_dbt_poc"].items():
        if(k==dag_name):
            print("dag name:",k)
            for k1, v1 in dataMap["airflow_dbt_poc"][k].items():
                if(k1!="dbt_tasks"):
                    dag_properties.append(k1)
            dag_property_value = {x:dataMap["airflow_dbt_poc"][k][x] for x in dag_properties}
    return dag_property_value
    
def get_dag_task_names(dataMap):
    dag_task_name=[]
    for k, v in dataMap["airflow_dbt_poc"].items():
        if(k==dag_name):
            print("dag name:",k)
            for k1, v1 in dataMap["airflow_dbt_poc"][k].items():
                if(k1=="dbt_tasks"):
                    
                    for dbt_k, dbt_v in dataMap["airflow_dbt_poc"][k][k1].items():
                        print("dbt module name:",dbt_k)
                        # print("Module name:",dbt_v["name"])
                        dag_task_name.append(dbt_v["name"])
                        print("Module name:",dbt_v["is_active_flag"])
    return dag_task_name
    
def make_dbt_task(node, dbt_verb,dag_properties, dag):
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


    return dbt_task

data = load_manifest()

dbt_tasks = {}
dataMap = load_config_yaml()
dag_properties = get_dag_properties(dataMap)
dag_task_name = get_dag_task_names(dataMap)
dag = DAG(
        dag_name,
        default_args=dag_properties,
        description='A dbt wrapper for airflow',
        schedule_interval=timedelta(days=1),
    )
for node in data["nodes"].keys():
    if node.split(".")[0] == "model" and node.split(".")[-1] in dag_task_name:
      #  node_test = node.replace("model", "test")

        dbt_tasks[node] = make_dbt_task(node, "build", dag_properties,dag)
       # dbt_tasks[node_test] = make_dbt_task(node, "test")

for node in data["nodes"].keys():
    if node.split(".")[0] == "model" and node.split(".")[-1] in dag_task_name:

        # Set dependency to run tests on a model after model runs finishes
       # node_test = node.replace("model", "test")
        #dbt_tasks[node] >> dbt_tasks[node_test]

        # Set all model -> model dependencies
        for upstream_node in data["nodes"][node]["depends_on"]["nodes"]:

            upstream_node_type = upstream_node.split(".")[0]
            if upstream_node_type == "model":
                dbt_tasks[upstream_node] >> dbt_tasks[node]