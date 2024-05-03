from yeeducli.utility.json_utils import response_validator, response_json_custom_order
from yeeducli.utility.logger_utils import Logger
from yeeducli.constants import TENANT_ORDER
from yeeducli import config
import requests
import sys

logger = Logger.get_logger(__name__, True)


class PlatformAdmin:
    def list_tenants():
        try:
            url = f"{config.YEEDU_RESTAPI_URL}/platform/admin/tenants"

            response = requests.request(
                "GET", url, headers=config.header_get, timeout=60, verify=False)
            if (response.status_code == 200 and isinstance(response.json(), list)):
                unordered_json = response.json()
                return response_json_custom_order(unordered_json, TENANT_ORDER), response.status_code
            else:
                return response_validator(response)
        except requests.exceptions.RequestException as e:
            logger.exception(f"Failed to connect due to {e}")
            sys.exit(-1)

    def add_tenant(json_data):
        try:
            url = f"{config.YEEDU_RESTAPI_URL}/platform/admin/tenant"

            response = requests.request(
                "POST", url, headers=config.headers, data=json_data, timeout=60, verify=False)
            return response_validator(response)
        except requests.exceptions.RequestException as e:
            logger.exception(f"Failed to connect due to {e}")
            sys.exit(-1)

    def get_tenant_by_id(id):
        try:
            url = f"{config.YEEDU_RESTAPI_URL}/platform/admin/tenant/{id}"

            response = requests.request(
                "GET", url, headers=config.header_get, timeout=60, verify=False)
            if (response.status_code == 200 and (isinstance(response.json(), dict) and response.json().get('error') is None)):
                unordered_json = response.json()
                return response_json_custom_order(unordered_json, TENANT_ORDER), response.status_code
            else:
                return response_validator(response)
        except requests.exceptions.RequestException as e:
            logger.exception(f"Failed to connect due to {e}")
            sys.exit(-1)

    def delete_tenant_by_id(id):
        try:
            url = f"{config.YEEDU_RESTAPI_URL}/platform/admin/tenant/{id}"

            response = requests.request(
                "DELETE", url, headers=config.header_get, verify=False)
            return response_validator(response)
        except requests.exceptions.RequestException as e:
            logger.exception(f"Failed to connect due to {e}")
            sys.exit(-1)

    def edit_tenant(id, json_data):
        try:
            url = f"{config.YEEDU_RESTAPI_URL}/platform/admin/tenant/{id}"

            response = requests.request(
                "PUT", url, headers=config.headers, data=json_data, timeout=60, verify=False)
            return response_validator(response)
        except requests.exceptions.RequestException as e:
            logger.exception(f"Failed to connect due to {e}")
            sys.exit(-1)

    def list_user_tenants(user_id):
        try:
            url = f"{config.YEEDU_RESTAPI_URL}/platform/admin/user/{user_id}/tenants"

            response = requests.request(
                "GET", url, headers=config.header_get, timeout=60, verify=False)
            return response_validator(response)
        except requests.exceptions.RequestException as e:
            logger.exception(f"Failed to connect due to {e}")
            sys.exit(-1)

    def search_tenant(name):
        try:
            url = f"{config.YEEDU_RESTAPI_URL}/platform/admin/search/tenant/{name}"

            response = requests.request(
                "GET", url, headers=config.header_get, timeout=60, verify=False)
            if (response.status_code == 200 and isinstance(response.json(), list)):
                unordered_json = response.json()
                return response_json_custom_order(unordered_json, TENANT_ORDER), response.status_code
            else:
                return response_validator(response)
        except requests.exceptions.RequestException as e:
            logger.exception(f"Failed to connect due to {e}")
            sys.exit(-1)
