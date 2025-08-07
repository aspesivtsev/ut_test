import requests
import logging 
import json
import os
import asyncio

from airflow.hooks.postgres_hook import PostgresHook
from psycopg2.extras import execute_values
from telegram.ext import ApplicationBuilder
#from airflow.hooks.base import BaseHook


def get_json_data():
    """Функция импорта из JSON в БД """
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    
    # источник загрузки данных (задал в коде, можно в Connections)
    conn_host = "https://raw.githubusercontent.com/sharmadhiraj/free-json-datasets/refs/heads/master/datasets/oscar-best-picture-award-winners.json"
    
    response = requests.get(conn_host, allow_redirects=True)
    
    # проверяем доступность
    response.raise_for_status()

    # сохраняем ответ
    response_json = response.json()
    
    if len(response_json)==0: # проверка на случай, если ответ 200, но json в ответе нет по какой-то причине
        logger.warning("No data available")
    else:
        # сохраняем JSON в БД
        pg_hook = PostgresHook(postgres_conn_id='dwh_conn', schema='dwh')
        connection = pg_hook.get_conn()
        cursor = connection.cursor()
        cursor.execute("truncate dwh_src.movies_raw_json")
        
        # парсим массив json "построчно" 
        data_to_insert = [(json.dumps(record),) for record in response_json]
        
        # вставляем сырые json-данные в таблицу dwh_src.movies_raw_json и коммитимся
        insert_query = "INSERT INTO dwh_src.movies_raw_json (data) VALUES %s"
        execute_values(cursor, insert_query, data_to_insert)
        connection.commit()
        cursor.close()
        connection.close()
        logger.info(f"DataFrame успешно сохранен в PostgreSQL! {len(data_to_insert)}")

async def _send_alert():
    # асинхронная функция отправки сообщения в ТГ
    TG_TOKEN : str = os.environ.get("TG_TOKEN")
    TG_CHAT_ID : str = os.environ.get("TG_CHAT_ID")
    application = ApplicationBuilder().token(TG_TOKEN).build()
    await application.bot.send_message(chat_id=TG_CHAT_ID, text="✅ DAG завершен!")

def send_telegram_message(**context):
    # отправка сообщения в ТГ
    asyncio.run(_send_alert())
