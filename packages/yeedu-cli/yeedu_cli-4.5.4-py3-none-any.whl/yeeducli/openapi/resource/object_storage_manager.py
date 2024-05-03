from yeeducli.utility.json_utils import response_validator, response_json_custom_order
from yeeducli.utility.logger_utils import Logger
from yeeducli.constants import OBJECT_STORAGE_MANAGER_ORDER
from yeeducli import config
import requests
import sys

logger = Logger.get_logger(__name__, True)


class ObjectStorageManager:
    def list_object_storage_manager(cloud_provider=None):
        try:
            if (cloud_provider == None):
                url = f"{config.YEEDU_RESTAPI_URL}/object_storage_manager"
            else:
                url = f"{config.YEEDU_RESTAPI_URL}/object_storage_manager?cloud_provider={cloud_provider}"

            response = requests.request(
                "GET", url, headers=config.header_get, timeout=200, verify=False)

            if (response.status_code == 200 and isinstance(response.json(), list)):
                unordered_json = response.json()
                return response_json_custom_order(unordered_json, OBJECT_STORAGE_MANAGER_ORDER), response.status_code
            else:
                return response_validator(response)
        except requests.exceptions.RequestException as e:
            logger.exception(f"Failed to connect due to {e}")
            sys.exit(-1)

    def get_object_storage_manager_by_object_storage_manager_id(object_storage_manager_id):
        try:
            url = f"{config.YEEDU_RESTAPI_URL}/object_storage_manager/{object_storage_manager_id}"

            response = requests.request(
                "GET", url, headers=config.header_get, timeout=60, verify=False)
            if (response.status_code == 200 and (isinstance(response.json(), dict) and response.json().get('error') is None)):
                unordered_json = response.json()
                return response_json_custom_order(unordered_json, OBJECT_STORAGE_MANAGER_ORDER), response.status_code
            else:
                return response_validator(response)
        except requests.exceptions.RequestException as e:
            logger.exception(f"Failed to connect due to {e}")
            sys.exit(-1)

    def add_object_storage_manager(json_data):
        try:
            url = f"{config.YEEDU_RESTAPI_URL}/object_storage_manager"

            response = requests.request(
                "POST", url, headers=config.headers, data=json_data, timeout=60, verify=False)

            return response_validator(response)
        except requests.exceptions.RequestException as e:
            logger.exception(f"Failed to connect due to {e}")
            sys.exit(-1)

    def edit_object_storage_manager(object_storage_manager_id, json_data):
        try:
            url = f"{config.YEEDU_RESTAPI_URL}/object_storage_manager/{object_storage_manager_id}"

            response = requests.request(
                "PUT", url, headers=config.headers, data=json_data, timeout=60, verify=False)

            return response_validator(response)
        except requests.exceptions.RequestException as e:
            logger.exception(f"Failed to connect due to {e}")
            sys.exit(-1)

    def delete_object_storage_manager(id):
        try:
            url = f"{config.YEEDU_RESTAPI_URL}/object_storage_manager/{id}"

            response = requests.request(
                "DELETE", url, headers=config.header_get, verify=False)

            return response_validator(response)
        except requests.exceptions.RequestException as e:
            logger.exception(f"Failed to connect due to {e}")
            sys.exit(-1)
