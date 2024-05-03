from yeeducli.utility.json_utils import response_validator, response_json_custom_order
from yeeducli.utility.logger_utils import Logger
from yeeducli.constants import BOOT_DISK_IMAGE_CONFIG_ORDER
from yeeducli import config
import requests
import sys

logger = Logger.get_logger(__name__, True)


class BootDiskImageConfiguration:

    def add_boot_disk_image_config(json_data):
        url = f"{config.YEEDU_RESTAPI_URL}/machine/boot_disk_image"

        try:
            response = requests.request(
                "POST", url, headers=config.headers, data=json_data, timeout=60, verify=False)
            return response_validator(response)
        except requests.exceptions.RequestException as e:
            logger.exception(f"Failed to connect due to {e}")
            sys.exit(-1)

    def list_boot_disk_image_config(cloud_provider=None):
        try:
            if cloud_provider is None:
                url = f"{config.YEEDU_RESTAPI_URL}/machine/boot_disk_image"
            else:
                url = f"{config.YEEDU_RESTAPI_URL}/machine/boot_disk_image?cloud_provider={cloud_provider}"
            response = requests.request(
                "GET", url, headers=config.header_get, timeout=60, verify=False)
            if (response.status_code == 200 and isinstance(response.json(), list)):
                unordered_json = response.json()
                return response_json_custom_order(unordered_json, BOOT_DISK_IMAGE_CONFIG_ORDER), response.status_code
            else:
                return response_validator(response)
        except requests.exceptions.RequestException as e:
            logger.exception(f"Failed to connect due to {e}")
            sys.exit(-1)

    def get_boot_disk_image_config_by_id(boot_disk_image_id):
        url = f'{config.YEEDU_RESTAPI_URL}/machine/boot_disk_image/{boot_disk_image_id}'
        try:
            response = requests.request(
                "GET", url, headers=config.header_get, timeout=60, verify=False)
            if (response.status_code == 200 and (isinstance(response.json(), dict) and response.json().get('error') is None)):
                unordered_json = response.json()
                return response_json_custom_order(unordered_json, BOOT_DISK_IMAGE_CONFIG_ORDER), response.status_code
            else:
                return response_validator(response)
        except requests.exceptions.RequestException as e:
            logger.exception(f"Failed to connect due to {e}")
            sys.exit(-1)
