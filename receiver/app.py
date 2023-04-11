import connexion
from connexion import NoContent
import datetime
import json
import logging
import logging.config
import pykafka
from pykafka import KafkaClient
import requests
import uuid
import yaml


with open("app_conf.yml", "r") as f:
    app_config = yaml.safe_load(
        f.read()
    )  # use yaml library to read the configuration file

with open("log_conf.yml", "r") as f:
    log_config = yaml.safe_load(f.read())
    logging.config.dictConfig(log_config)


def process_event(event, endpoint):
    trace_id = str(uuid.uuid4())
    event["trace_id"] = trace_id

    logger.debug(f"Received {endpoint} event with trace id {trace_id}")

    hosts = app_config["events"]["hostname"] + ":" + str(app_config["events"]["port"])
    client = KafkaClient(hosts=hosts)

    topic = client.topics[app_config["events"]["topic"]]

    producer = topic.get_sync_producer()  # create a Kafka producer using the topic

    event_dict = {
        "type": endpoint,
        "datetime": datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ"),
        "payload": event,
    }

    event_json = json.dumps(event_dict)

    producer.produce(event_json.encode("utf-8"))

    logger.debug(f"PRODUCER::producing x {endpoint}")
    logger.debug(f"{event_json}")
    return NoContent, 201


# Endpoints
def buy(body):
    process_event(body, "buy")
    return NoContent, 201


def sell(body):
    process_event(body, "sell")
    return NoContent, 201


def health():
    return "200 OK", 200


app = connexion.FlaskApp(__name__, specification_dir="")
app.add_api(
    "openapi.yml",
    base_path="/receiver",
    strict_validation=True,
    validate_responses=True,
)


logger = logging.getLogger("basic")

if __name__ == "__main__":
    app.run(port=8080)
