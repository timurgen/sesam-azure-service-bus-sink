import os
import logging
import json

from azure.servicebus.control_client import ServiceBusService, Message
from waitress import serve
from flask import Flask, Response, request, abort

APP = Flask(__name__)

log_level = logging.getLevelName(os.environ.get("LOG_LEVEL", "INFO"))
logging.basicConfig(level=log_level)

SERVICE_NAMESPACE = os.environ.get("SERVICE_NAMESPACE")
PAYLOAD_KEY = os.environ.get("PAYLOAD_KEY")

if not SERVICE_NAMESPACE:
    logging.error("namespace must be provided")
    exit(1)


@APP.route("/<queue_name>", methods=['POST'])
def process_request(queue_name):
    """
    Endpoint to publish messages to Azure service bus
    :param queue_name: name of queue to publish messages to
    :return:
    """
    input_data = request.get_json()
    bus_service = ServiceBusService(service_namespace=SERVICE_NAMESPACE,
                                    shared_access_key_name=request.headers.get('sas-token-name'),
                                    shared_access_key_value=request.headers.get('sas-token'))

    for index, input_entity in enumerate(input_data):
        data: str = json.dumps(input_entity[PAYLOAD_KEY] if PAYLOAD_KEY else input_entity).encode(
            "utf-8")
        msg = Message(data)
        try:
            bus_service.send_queue_message(queue_name, msg)
            logging.info("Entity %s sent successfully", input_entity["_id"])
        except Exception as e:
            logging.error(e)
            abort(500)
    return Response()


if __name__ == "__main__":
    port = os.environ.get('PORT', 5000)
    logging.info("starting service on port %d", port)
    serve(APP, host='0.0.0.0', port=port)
