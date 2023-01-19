import connexion
from connexion import NoContent
from datetime import datetime
import json
import logging
import logging.config
import pykafka
from pykafka import KafkaClient
import requests
import uuid
import yaml

# TODO - create array to store incoming JSON buy/sell objects

data = []


def process_events(event):
    # TODO
    # Use datetime and strftime to create a string representing the current
    # date and time (see openapi.yml for format)
    current_datetime = datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")

    # Create a uuid called trace_id using the uuid.uuid4() function,
    # and append it to the event parameter
    trace_id = uuid.uuid4()
    event["trace_id"] = str(trace_id)

    # Create an object named 'obj' with three properties:
    # received_timestamp (value is the current date and time created above)
    # event_data (value is a string containing all values from the event parameter,
    # including your trace_id)
    obj = {
        "received_timestamp": current_datetime,
        "event_data": event,
    }

    # if array length is less than 10, add your object (obj) to the array
    if len(data) < 10:
        data.insert(0, obj)

    # If array length equals ten,
    # remove last object from the array and insert your new object (obj) at the beginning,
    elif len(data) == 10:
        data.pop(-1)
        data.insert(0, obj)

    # then write the entire array to a file named events.json
    #
    # note: you are allowed to overwrite the contents of events.json each time you write

    with open("events.json", "w") as f:
        json_string = json.dumps(data)
        f.write(json_string)

    # TODO - return obj
    return obj


# Endpoints
def buy(body):
    # TODO - pass the body parameter to your process_events function
    process_events(body)
    return NoContent, 201


def sell(body):
    # TODO - pass the body parameter to your process_events function
    process_events(body)
    return NoContent, 201


app = connexion.FlaskApp(__name__, specification_dir="")
app.add_api("openapi.yml", strict_validation=True, validate_responses=True)

if __name__ == "__main__":
    app.run(port=8080)
