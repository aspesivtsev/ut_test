from airflow.models import Connection
from airflow import settings


def create_dwh_connection():
    """ Создаем объект соединения для тестирования, в продакшене такого не делаем"""
    conn = Connection(
        conn_id='dwh_conn',
        conn_type='postgres',
        host='postgres_database',
        login='dwh_user',
        password='QPY9DQyg4rhya9xcEuP1',
        port=5432,
        schema="dwh"
    )

    session = settings.Session()
    if session.query(Connection).filter(Connection.conn_id == conn.conn_id).first():
        return  # соединение уже существует
    session.add(conn)
    session.commit()
    session.close()

def create_http_connection():
    """Создаем объект соединения с источником данных для тестирования, в продакшене такого не делаем"""
    conn = Connection(
        conn_id = "http_source_json",
        conn_type = "http",
        host = "https://raw.githubusercontent.com/sharmadhiraj/free-json-datasets/refs/heads/master/datasets/"
    )

    session = settings.Session()
    if session.query(Connection).filter(Connection.conn_id == conn.conn_id).first():
        return  # соединение уже существует
    session.add(conn)
    session.commit()
    session.close()
