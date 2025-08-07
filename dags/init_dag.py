import logging

from airflow import DAG
from airflow.operators.dummy import DummyOperator
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from airflow.providers.common.sql.operators.sql import SQLExecuteQueryOperator
from datetime import datetime, timedelta
from airflow.models.baseoperator import chain
from libs.create_dwh_connection import create_dwh_connection, create_http_connection
#from airflow.providers.postgres.operators.postgres import PostgresOperator


logger = logging.getLogger('airflow.task')
logger.debug

args = {
    'owner': 'UT',
    'depends_on_past': False,
    'email': ['spesivcev@sochi-park.ru'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 0,
    'retry_delay': timedelta(minutes=1),
}

with DAG(
    'run_first_db_and_connection_init',
    default_args=args,
    description='Создание структуры БД и соединения к БД',
    schedule=None,
    catchup = False,
    start_date = datetime.now() - timedelta(days=1),
    max_active_runs=1,
    tags=['INIT'],
) as dag:

    start_task = DummyOperator(
    task_id="starting_the_process"
    )

    create_dwh_connection_task = PythonOperator(
    task_id="create_dwh_connection",
    python_callable=create_dwh_connection
    )
    create_http_connection_task = PythonOperator(
    task_id="create_http_connection",
    python_callable=create_http_connection
    )
    create_init_db_structure = SQLExecuteQueryOperator(
    task_id = 'create_init_db_structure',
    conn_id='dwh_conn',
    sql='sql/init_db_structure.sql',
    autocommit=True
    )

    run_dbt_deps = BashOperator(
        task_id='run_dbt_deps',
        bash_command="""
        cd /opt/airflow/dbt && dbt deps
        """,
    )

    end_task = DummyOperator(
    task_id="ending_the_process"
    )

# start_task >> create_dwh_connection_task >> create_http_connection_task >> create_init_db_structure >> run_dbt_deps >> end_task

chain(
    start_task,
    create_dwh_connection_task,
    create_http_connection_task,
    create_init_db_structure,
    run_dbt_deps,
    end_task
)