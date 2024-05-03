from yeeducli.utility.json_utils import response_validator, response_json_custom_order
from yeeducli.utility.logger_utils import Logger
from yeeducli.constants import MACHINE_CONFIG_ORDER
from yeeducli import config
import requests
import sys

logger = Logger.get_logger(__name__, True)


class MachineConfiguration:
    def list_machine_config(cloud_provider=None):
        if cloud_provider == None:
            url = f"{config.YEEDU_RESTAPI_URL}/machine"
        else:
            url = f"{config.YEEDU_RESTAPI_URL}/machine?cloud_provider={cloud_provider}"
        try:
            response = requests.request(
                "GET", url, headers=config.header_get, timeout=60, verify=False)
            if (response.status_code == 200 and isinstance(response.json(), list)):
                unordered_json = response.json()
                return response_json_custom_order(unordered_json, MACHINE_CONFIG_ORDER), response.status_code
            else:
                return response_validator(response)
        except requests.exceptions.RequestException as e:
            logger.exception(f"Failed to connect due to {e}")
            sys.exit(-1)

    def add_machine_config(json_data):
        url = f"{config.YEEDU_RESTAPI_URL}/machine"
        try:
            response = requests.request(
                "POST", url, headers=config.headers, data=json_data, timeout=60, verify=False)
            return response_validator(response)
        except requests.exceptions.RequestException as e:
            logger.exception(f"Failed to connect due to {e}")
            sys.exit(-1)

    def get_machine_config_by_id(machine_conf_id):
        url = f"{config.YEEDU_RESTAPI_URL}/machine/{machine_conf_id}"
        try:
            response = requests.request(
                "GET", url, headers=config.header_get, timeout=60, verify=False)
            if (response.status_code == 200 and (isinstance(response.json(), dict) and response.json().get('error') is None)):
                unordered_json = response.json()
                return response_json_custom_order(unordered_json, MACHINE_CONFIG_ORDER), response.status_code
            else:
                return response_validator(response)
        except requests.exceptions.RequestException as e:
            logger.exception(f"Failed to connect due to {e}")
            sys.exit(-1)

    def edit_machine_config(machine_conf_id, json_data):
        url = f"{config.YEEDU_RESTAPI_URL}/machine/{machine_conf_id}"
        try:
            response = requests.request(
                "PUT", url, headers=config.headers, data=json_data, timeout=60, verify=False)
            return response_validator(response)
        except requests.exceptions.RequestException as e:
            logger.exception(f"Failed to connect due to {e}")
            sys.exit(-1)
