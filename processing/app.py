import connexion
from connexion import NoContent
import datetime
import json
import logging
import logging.config
import requests
import yaml
import apscheduler
from apscheduler.schedulers.background import BackgroundScheduler

import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from base import Base
from stats import Stats
from flask_cors import CORS  # CORS is a function


DB_ENGINE = create_engine("sqlite:///stats.sqlite")
Base.metadata.bind = DB_ENGINE
DB_SESSION = sessionmaker(bind=DB_ENGINE)


def get_latest_stats():
    session = DB_SESSION()

    result = session.query(Stats).order_by(Stats.last_updated.desc()).first()
    data = result.to_dict()
    return data


def populate_stats():

    timestamp = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
    last_updated = timestamp
    print(last_updated)

    session = DB_SESSION()

    data = get_latest_stats()

    last_updated = data["last_updated"]

    events = requests.get(f"http://74.235.55.16/storage/buy?timestamp={last_updated}")

    event = events.json()
    for e in event:
        data["num_buys"] += e["buy_qty"]
        if e["item_price"] > data["max_buy_price"]:
            data["max_buy_price"] = e["item_price"]

    events = requests.get(f"http://74.235.55.16/storage/sell?timestamp={last_updated}")

    event = events.json()
    for e in event:
        data["num_sells"] += e["sell_qty"]
        if e["item_price"] > data["max_sell_price"]:
            data["max_sell_price"] = e["item_price"]

    data["last_updated"] = timestamp

    stats = Stats(**data)

    session.add(stats)
    session.commit()
    session.close()

    return NoContent, 201


def init_scheduler():
    sched = BackgroundScheduler(daemon=True)
    sched.add_job(populate_stats, "interval", seconds=app_config["period"])
    sched.start()


def health():
    return "200 OK", 200


app = connexion.FlaskApp(__name__, specification_dir="")
app.add_api(
    "openapi.yml",
    base_path="/processing",
    strict_validation=True,
    validate_responses=True,
)
CORS(app.app)

with open("app_conf.yml", "r") as f:
    app_config = yaml.safe_load(f.read())

with open("log_conf.yml", "r") as f:
    log_config = yaml.safe_load(f.read())
    logging.config.dictConfig(log_config)

logger = logging.getLogger("basic")

if __name__ == "__main__":
    init_scheduler()
    app.run(port=8100, use_reloader=False)
