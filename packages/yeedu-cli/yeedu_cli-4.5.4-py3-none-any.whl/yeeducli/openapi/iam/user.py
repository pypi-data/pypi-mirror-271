from yeeducli.utility.json_utils import response_validator
from yeeducli.utility.logger_utils import Logger
from yeeducli import config
import requests
import sys

logger = Logger.get_logger(__name__, True)


class User:
    def list_tenants():
        try:
            url = f"{config.YEEDU_RESTAPI_URL}/user/tenants"

            response = requests.request(
                "GET", url, headers=config.header_get, timeout=60, verify=False)
            return response_validator(response)
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to connect due to {e}")
            sys.exit(-1)

    def associate_tenant(tenant_id):
        try:
            url = f"{config.YEEDU_RESTAPI_URL}/user/select/{tenant_id}"

            response = requests.request(
                "POST", url, headers=config.headers, timeout=60, verify=False)
            return response_validator(response)
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to connect due to {e}")
            sys.exit(-1)

    def get_user_info():
        try:
            url = f"{config.YEEDU_RESTAPI_URL}/user/info"

            response = requests.request(
                "GET", url, headers=config.header_get, timeout=60, verify=False)
            return response_validator(response)
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to connect due to {e}")
            sys.exit(-1)

    def get_user_roles():
        try:
            url = f"{config.YEEDU_RESTAPI_URL}/user/info/roles"

            response = requests.request(
                "GET", url, headers=config.headers, timeout=60, verify=False)
            return response_validator(response)
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to connect due to {e}")
            sys.exit(-1)
