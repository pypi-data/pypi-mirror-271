import os
import json
from jsonschema import validate
from wiliot_deployment_tools.ag.ut_defines import GW_CONF, GW_API_VERSION
import pkg_resources

from enum import Enum

class MESSAGE_TYPES(Enum):
    STATUS = "status"
    DATA = "data"
    LOGS = "logs"
FALLBACK_API = "200"

def validate_message(message_type: MESSAGE_TYPES, message: dict) -> tuple[bool, str]:
    """
    Validate MQTT message
    :type message_type: MESSAGE_TYPES
    :param message_type: MQTT message type
    :type message: dict
    :param message: MQTT Message
    :return: tuple (bool, str)
    """
    try:
        api_version = message[GW_CONF][GW_API_VERSION]
    except KeyError:
        api_version = FALLBACK_API
    json_path = pkg_resources.resource_filename(__name__, f"{api_version}/{message_type.value}.json")
    with open(json_path) as f:
        schema = json.load(f)
    try:
        validate(message, schema)
        return (True, None)
    except Exception as e:
        return (False, e.message)