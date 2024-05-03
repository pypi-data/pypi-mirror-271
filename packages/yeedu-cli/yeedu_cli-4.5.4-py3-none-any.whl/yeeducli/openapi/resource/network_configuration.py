from yeeducli.utility.json_utils import response_validator, response_json_custom_order
from yeeducli.utility.logger_utils import Logger
from yeeducli.constants import NETWORK_CONFIG_ORDER
from yeeducli import config
import requests
import sys

logger = Logger.get_logger(__name__, True)


class NetworkConfiguration:
    def get_network_config_by_cp_id(cloud_provider=None):
        try:
            if cloud_provider is None:
                url = f"{config.YEEDU_RESTAPI_URL}/machine/network"
            else:
                url = f"{config.YEEDU_RESTAPI_URL}/machine/network?cloud_provider={cloud_provider}"

            response = requests.request(
                "GET", url, headers=config.header_get, timeout=60, verify=False)
            if (response.status_code == 200 and isinstance(response.json(), list)):
                unordered_json = response.json()
                return response_json_custom_order(unordered_json, NETWORK_CONFIG_ORDER), response.status_code
            else:
                return response_validator(response)
        except requests.exceptions.RequestException as e:
            logger.exception(f"Failed to connect due to {e}")
            sys.exit(-1)

    def add_network_config_by_cp_id(cloud_provider_id, json_data):
        try:
            url = f"{config.YEEDU_RESTAPI_URL}/machine/network"
            response = requests.request(
                "POST", url, headers=config.headers, data=json_data, timeout=60, verify=False)
            return response_validator(response)
        except requests.exceptions.RequestException as e:
            logger.exception(f"Failed to connect due to {e}")
            sys.exit(-1)

    def get_network_config_by_cp_id_and_id(network_conf_id):
        try:
            url = f"{config.YEEDU_RESTAPI_URL}/machine/network/{network_conf_id}"
            response = requests.request(
                "GET", url, headers=config.header_get, timeout=60, verify=False)
            if (response.status_code == 200 and (isinstance(response.json(), dict) and response.json().get('error') is None)):
                unordered_json = response.json()
                return response_json_custom_order(unordered_json, NETWORK_CONFIG_ORDER), response.status_code
            else:
                return response_validator(response)
        except requests.exceptions.RequestException as e:
            logger.exception(f"Failed to connect due to {e}")
            sys.exit(-1)

    def modify_network_config_by_cp_id_and_id(network_conf_id, json_data):
        try:
            url = f"{config.YEEDU_RESTAPI_URL}/machine/network/{network_conf_id}"
            response = requests.request(
                "PUT", url, headers=config.headers, data=json_data, timeout=60, verify=False)
            return response_validator(response)
        except requests.exceptions.RequestException as e:
            logger.exception(f"Failed to connect due to {e}")
            sys.exit(-1)
