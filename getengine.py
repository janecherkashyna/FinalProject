from sqlalchemy import create_engine
from db_config import config

db_info = config()

engine = create_engine(f'postgresql+psycopg2://{db_info["user"]}:'
                       f'{db_info["password"]}@{db_info["host"]}:'
                       f'{db_info["port"]}/{db_info["database"]}')

