import logging 

from airflow import DAG
from airflow.operators.dummy import DummyOperator
from airflow.operators.python import PythonOperator
from airflow.providers.http.sensors.http import HttpSensor
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta
from libs.get_data_from_source import get_json_data, send_telegram_message


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
    'get_json_data_from_oscar_best_picture_award_winners',
    default_args=args,
    description='DAG запускается в 9:30 по понедельникам, средам и пятницам',
    schedule='30 6 * * 1,3,5',  # Запуск в 6:30 UTC (в 9:30 по Москве GMT+3) пн[1], ср[3], пт[5]
    catchup = False,
    start_date = datetime.now() - timedelta(days=1),
    max_active_runs=1,
    tags=['source >> SRC'],
) as dag:

    start_task = DummyOperator(
    task_id="starting_the_process"
    )

    is_json_available = HttpSensor(
    task_id='is_json_available',
    http_conn_id='http_source_json',
    endpoint='oscar-best-picture-award-winners.json'
    )

    process_task = PythonOperator(
    task_id="processing_the_data",
    python_callable=get_json_data
    )

    run_dbt_tasks = BashOperator(
    task_id='run_dbt_tasks',
    bash_command="""
    cd /opt/airflow/dbt && dbt run --select movies_raw movies directors stars movie_directors movie_stars
    """
    )

    send_telegram_alert = PythonOperator(
            task_id='send_telegram_alert',
            python_callable=send_telegram_message,
            provide_context=True
    )

    end_task = DummyOperator(
    task_id="ending_the_process"
    )

start_task >> is_json_available >> process_task >> run_dbt_tasks >> send_telegram_alert >> end_task
