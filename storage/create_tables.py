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
    CREATE TABLE buy
    (id INT NOT NULL AUTO_INCREMENT,
    buy_id VARCHAR(250) NOT NULL,
    item_name VARCHAR(250) NOT NULL,
    item_price FLOAT NOT NULL,
    buy_qty INTEGER NOT NULL,
    trace_id VARCHAR(100) NOT NULL,
    date_created VARCHAR(100) NOT NULL,
    CONSTRAINT buy_pk PRIMARY KEY (id))
"""
)

db_cursor.execute(
    """
    CREATE TABLE sell
    (id INT NOT NULL AUTO_INCREMENT,
    sell_id VARCHAR(250) NOT NULL,
    item_name VARCHAR(250) NOT NULL,
    item_price FLOAT NOT NULL,
    sell_qty INTEGER NOT NULL,
    trace_id VARCHAR(100) NOT NULL,
    date_created VARCHAR(100) NOT NULL,
    CONSTRAINT sell_pk PRIMARY KEY (id))
"""
)

db_conn.commit()
db_conn.close()
