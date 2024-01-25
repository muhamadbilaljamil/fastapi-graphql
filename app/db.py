from orator import DatabaseManager, Schema, Model
# import orator
from .config import settings

DATABASES = {
    "postgres": {
        "driver": settings.POSTGRES_DRIVER,
        "host": settings.POSTGRES_SERVER,
        "database": settings.POSTGRES_DB,
        "user": settings.POSTGRES_USER,
        "password": settings.POSTGRES_PASSWORD,
        "prefix": "",
        "port": settings.POSTGRES_PORT,
    }
}

db = DatabaseManager(DATABASES)
schema = Schema(db)
Model.set_connection_resolver(db)

# use python stable version

# python3 -m venv env  make virtual environment 

# source env/bin/activate  active virtual environment

# pip freeze > requirements.txt  save installed packages in file

# pip install -r requirements.txt  install in other computer
