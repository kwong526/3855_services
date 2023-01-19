import sqlite3

conn = sqlite3.connect("events.sqlite")
c = conn.cursor()

sql = """CREATE TABLE buy_event
    (id INT PRIMARY KEY AUTO_INCREMENT,
    buy_id VARCHAR(250) NOT NULL,
    item_name VARCHAR(250) NOT NULL, 
    item_price FLOAT(15,2) NOT NULL,
    buy_qty INTEGER NOT NULL,
    trace_id VARCHAR(250) NOT NULL
    """
c.execute(sql)

sql = """CREATE TABLE sell_event
    (id INT PRIMARY KEY AUTO_INCREMENT,
    sell_id VARCHAR(250) NOT NULL,
    item_name VARCHAR(250) NOT NULL, 
    item_price FLOAT(15,2) NOT NULL,
    sell_qty INTEGER NOT NULL,
    trace_id VARCHAR(250) NOT NULL
    """
c.execute(sql)

conn.commit()
conn.close()
