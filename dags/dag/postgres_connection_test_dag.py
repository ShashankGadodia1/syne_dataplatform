from airflow.operators.postgres_operator import PostgresOperator
import datetime
import json

from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.utils.dates import datetime
from airflow.utils.dates import timedelta


default_args = {
    'owner': 'shashank',
    'depends_on_past': False,
    'start_date': datetime(2023, 12, 8),
    'email': ['shashank.gadodia@gmail.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 0,
    'catchup': False,
    'retry_delay': timedelta(minutes=5)
}


dag = DAG(
    'postgres_connection_test_dag',
    default_args=default_args,
    description='testing db',
    schedule_interval=timedelta(days=1),
)

task_sql = """
-- Your SQL Query here
create schema config;
create table postgres.config.dummy (name varchar);
insert into postgres.config.dummy values( '1');
"""

task_postgres = PostgresOperator(
    task_id='postgres_connection_test',
    sql=task_sql,
    postgres_conn_id='postgres_metadata',  # Specify the connection ID
    autocommit=True,
    dag=dag,
)