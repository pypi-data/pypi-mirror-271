from yeeducli.utility.json_utils import response_validator
from yeeducli.utility.logger_utils import Logger
from yeeducli import config
import requests
import sys

logger = Logger.get_logger(__name__, True)


class SharedPlatformAndAdmin:
    def sync_user(username):
        try:
            url = f"{config.YEEDU_RESTAPI_URL}/platform/shared/admin/sync/user/{username}"

            response = requests.request(
                "GET", url, headers=config.header_get, timeout=60, verify=False)
            return response_validator(response)
        except requests.exceptions.RequestException as e:
            logger.exception(f"Failed to connect due to {e}")
            sys.exit(-1)

    def sync_group(groupname):
        try:
            url = f"{config.YEEDU_RESTAPI_URL}/platform/shared/admin/sync/group/{groupname}"

            response = requests.request(
                "GET", url, headers=config.header_get, timeout=60, verify=False)
            return response_validator(response)
        except requests.exceptions.RequestException as e:
            logger.exception(f"Failed to connect due to {e}")
            sys.exit(-1)

    def get_all_user_groups(user_id=None):
        try:
            url = f"{config.YEEDU_RESTAPI_URL}/platform/shared/admin/user/{user_id}/groups"

            response = requests.request(
                "GET", url, headers=config.header_get, timeout=200, verify=False)
            return response_validator(response)
        except requests.exceptions.RequestException as e:
            logger.exception(f"Failed to connect due to {e}")
            sys.exit(-1)

    def list_users():
        try:
            url = f"{config.YEEDU_RESTAPI_URL}/platform/shared/admin/users"

            response = requests.request(
                "GET", url, headers=config.header_get, timeout=200, verify=False)
            return response_validator(response)
        except requests.exceptions.RequestException as e:
            logger.exception(f"Failed to connect due to {e}")
            sys.exit(-1)

    def get_all_group_users(group_id=None):
        try:
            url = f"{config.YEEDU_RESTAPI_URL}/platform/shared/admin/group/{group_id}/users"

            response = requests.request(
                "GET", url, headers=config.header_get, timeout=200, verify=False)
            return response_validator(response)
        except requests.exceptions.RequestException as e:
            logger.exception(f"Failed to connect due to {e}")
            sys.exit(-1)

    def list_groups():
        try:
            url = f"{config.YEEDU_RESTAPI_URL}/platform/shared/admin/groups"

            response = requests.request(
                "GET", url, headers=config.header_get, timeout=200, verify=False)
            return response_validator(response)
        except requests.exceptions.RequestException as e:
            logger.exception(f"Failed to connect due to {e}")
            sys.exit(-1)

    def search_users(username):
        try:
            url = f"{config.YEEDU_RESTAPI_URL}/platform/shared/admin/search/users/{username}"

            response = requests.request(
                "GET", url, headers=config.header_get, timeout=60, verify=False)
            return response_validator(response)
        except requests.exceptions.RequestException as e:
            logger.exception(f"Failed to connect due to {e}")
            sys.exit(-1)

    def search_groups(groupname):
        try:
            url = f"{config.YEEDU_RESTAPI_URL}/platform/shared/admin/search/groups/{groupname}"

            response = requests.request(
                "GET", url, headers=config.header_get, timeout=60, verify=False)
            return response_validator(response)
        except requests.exceptions.RequestException as e:
            logger.exception(f"Failed to connect due to {e}")
            sys.exit(-1)
