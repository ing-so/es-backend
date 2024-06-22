# cf) pip3 install tuya-connector-python

import time
import logging
from tuya_connector import TuyaOpenAPI, TUYA_LOGGER

ACCESS_ID = "############"
ACCESS_KEY = "#################"
API_ENDPOINT = "https://#############"

TUYA_LOGGER.setLevel(logging.DEBUG)

openapi = TuyaOpenAPI(API_ENDPOINT, ACCESS_ID, ACCESS_KEY)

def lambda_handler(event, context):
    openapi.connect()
    DEVICE_ID = "eb9073jooyzi16bn"

    try:
        response = openapi.get("/v1.0/iot-03/devices/{}".format(DEVICE_ID))
        logging.info("Device Information: %s", response)

        response = openapi.get("/v1.0/iot-03/devices/{}/functions".format(DEVICE_ID))
        logging.info("Device Functions: %s", response)

        # 5초 쉬기
        time.sleep(10)

        commands = {
            "commands": [
                {"code": "switch", "value": True},
                {"code": "mode", "value": "click"},
                {"code": "click_sustain_time", "value": 2},
                {"code": "arm_down_percent", "value": 0},
                {"code": "arm_up_percent", "value": 0}
            ]
        }
        response = openapi.post('/v1.0/iot-03/devices/{}/commands'.format(DEVICE_ID), commands)
        logging.info("Command Response: %s", response)

        response = openapi.get("/v1.0/iot-03/devices/{}/status".format(DEVICE_ID))
        logging.info("Device Status: %s", response)

        return {
            'statusCode': 200,
            'body': 'Success'
        }

    except Exception as e:
        logging.error("Error: %s", str(e))
        return {
            'statusCode': 500,
            'body': str(e)
        }
