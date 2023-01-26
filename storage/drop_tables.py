import mysql.connector
import yaml

with open("app_conf.yml", "r") as f:
    app_config = yaml.safe_load(f.read())

db_conn = mysql.connector.connect(
    host=app_config["hostname"],
    user=app_config["user"],
    password=app_config["password"],
    database=app_config["db"],
)
db_cursor = db_conn.cursor()

db_cursor.execute(
    """
    DROP TABLE buy, sell
"""
)

db_conn.commit()
db_conn.close()
