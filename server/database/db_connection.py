from peewee import *
import os
import config

db = PostgresqlDatabase(
    database=os.getenv('DB_NAME', config.datebase_name), 
    host=os.getenv('DB_IP', config.datebase_host),
    port=int(os.getenv('DB_PORT', config.datebase_port)),
    user=os.getenv('DB_USERNAME', config.datebase_user), 
    password=os.getenv('DB_PASSWORD', config.datebase_pw)
)

