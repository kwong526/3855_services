import datetime
import json

import connexion
from connexion import NoContent
import swagger_ui_bundle

import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from base import Base
from buy import Buy
from sell import Sell

DB_ENGINE = create_engine("sqlite:///events.sqlite")
Base.metadata.bind = DB_ENGINE
DB_SESSION = sessionmaker(bind=DB_ENGINE)

# Endpoints
def buy(body):
    """receives a buy event"""
    session = DB_SESSION()

    # TODO create a Buy object and populate it with values from the body
    buy_event = Buy(
        body["buy_id"],
        body["item_name"],
        body["item_price"],
        body["buy_qty"],
        body["date_created"],
    )
    # TODO add, commit, and close the session
    session.add(buy_event)
    session.commit()
    session.close()

    return NoContent, 201


def get_buys():
    # placeholder for future labs
    pass


def sell(body):
    session = DB_SESSION()

    # TODO create a Buy object and populate it with values from the body
    sell_event = Sell(
        body["sell_id"],
        body["item_name"],
        body["item_price"],
        body["sell_qty"],
        body["date_created"],
    )
    # TODO add, commit, and close the session
    session.add(sell_event)
    session.commit()
    session.close()

    return NoContent, 201


def get_sells():
    # placeholder for future labs
    pass


app = connexion.FlaskApp(__name__, specification_dir="")
app.add_api("openapi.yaml", strict_validation=True, validate_responses=True)

if __name__ == "__main__":
    app.run(port=8090)
