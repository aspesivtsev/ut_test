import os

class Settings:
    PROJECT_NAME:str = "API for UT"
    PROJECT_VERSION: str = "1.0.0"

    POSTGRES_USER : str = os.environ.get("POSTGRES_USER_DB")
    POSTGRES_PASSWORD = os.environ.get("POSTGRES_PASSWORD_DB")
    POSTGRES_SERVER : str = os.environ.get("POSTGRES_DB_SERVER")
    POSTGRES_PORT : str = os.environ.get("POSTGRES_DB_PORT") # default postgres port is 5432
    POSTGRES_DB : str = os.environ.get("POSTGRES_DB_DWH")
    DATABASE_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}:{POSTGRES_PORT}/{POSTGRES_DB}?options=-csearch_path=dwh_ods"

settings = Settings()

# print(settings.DATABASE_URL)
