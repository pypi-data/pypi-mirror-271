from yeeducli.utility.json_utils import response_validator
from yeeducli.utility.logger_utils import Logger
from yeeducli import config
import requests
import sys

logger = Logger.get_logger(__name__, True)


class CommonPlatformAndAdmin:
    def list_tenant_users(pageNumber, limit, tenant_id=None):
        try:
            if tenant_id is None:
                url = f"{config.YEEDU_RESTAPI_URL}/admin/users?pageNumber={pageNumber}&limit={limit}"
            else:
                url = f"{config.YEEDU_RESTAPI_URL}/platform/admin/tenant/{tenant_id}/users?pageNumber={pageNumber}&limit={limit}"

            response = requests.request(
                "GET", url, headers=config.header_get, timeout=60, verify=False)
            return response_validator(response)
        except requests.exceptions.RequestException as e:
            logger.exception(f"Failed to connect due to {e}")
            sys.exit(-1)

    def get_tenant_user(user_id, tenant_id=None):
        try:
            if tenant_id is None:
                url = f"{config.YEEDU_RESTAPI_URL}/admin/user/{user_id}"
            else:
                url = f"{config.YEEDU_RESTAPI_URL}/platform/admin/tenant/{tenant_id}/user/{user_id}"

            response = requests.request(
                "GET", url, headers=config.header_get, timeout=60, verify=False)
            return response_validator(response)
        except requests.exceptions.RequestException as e:
            logger.exception(f"Failed to connect due to {e}")
            sys.exit(-1)

    def get_user_roles(user_id, tenant_id=None):
        try:
            if tenant_id is None:
                url = f"{config.YEEDU_RESTAPI_URL}/admin/user/{user_id}/roles"
            else:
                url = f"{config.YEEDU_RESTAPI_URL}/platform/admin/tenant/{tenant_id}/user/{user_id}/roles"

            response = requests.request(
                "GET", url, headers=config.header_get, timeout=60, verify=False)
            return response_validator(response)
        except requests.exceptions.RequestException as e:
            logger.exception(f"Failed to connect due to {e}")
            sys.exit(-1)

    def list_user_roles(pageNumber, limit, tenant_id=None):
        try:
            if tenant_id is None:
                url = f"{config.YEEDU_RESTAPI_URL}/admin/roles/users?pageNumber={pageNumber}&limit={limit}"
            else:
                url = f"{config.YEEDU_RESTAPI_URL}/platform/admin/tenant/{tenant_id}/roles/users?pageNumber={pageNumber}&limit={limit}"

            response = requests.request(
                "GET", url, headers=config.header_get, timeout=60, verify=False)
            return response_validator(response)
        except requests.exceptions.RequestException as e:
            logger.exception(f"Failed to connect due to {e}")
            sys.exit(-1)

    def get_role_users(role_id, tenant_id=None):
        try:
            if tenant_id is None:
                url = f"{config.YEEDU_RESTAPI_URL}/admin/roles/users/{role_id}"
            else:
                url = f"{config.YEEDU_RESTAPI_URL}/platform/admin/tenant/{tenant_id}/roles/users/{role_id}"

            response = requests.request(
                "GET", url, headers=config.header_get, timeout=60, verify=False)
            return response_validator(response)
        except requests.exceptions.RequestException as e:
            logger.exception(f"Failed to connect due to {e}")
            sys.exit(-1)

    def list_tenant_groups(pageNumber, limit, tenant_id=None):
        try:
            if tenant_id is None:
                url = f"{config.YEEDU_RESTAPI_URL}/admin/groups?pageNumber={pageNumber}&limit={limit}"
            else:
                url = f"{config.YEEDU_RESTAPI_URL}/platform/admin/tenant/{tenant_id}/groups?pageNumber={pageNumber}&limit={limit}"

            response = requests.request(
                "GET", url, headers=config.header_get, timeout=60, verify=False)
            return response_validator(response)
        except requests.exceptions.RequestException as e:
            logger.exception(f"Failed to connect due to {e}")
            sys.exit(-1)

    def get_tenant_group(group_id, tenant_id=None):
        try:
            if tenant_id is None:
                url = f"{config.YEEDU_RESTAPI_URL}/admin/groups/{group_id}"
            else:
                url = f"{config.YEEDU_RESTAPI_URL}/platform/admin/tenant/{tenant_id}/group/{group_id}"

            response = requests.request(
                "GET", url, headers=config.header_get, timeout=60, verify=False)
            return response_validator(response)
        except requests.exceptions.RequestException as e:
            logger.exception(f"Failed to connect due to {e}")
            sys.exit(-1)

    def get_group_roles(group_id, tenant_id=None):
        try:
            if tenant_id is None:
                url = f"{config.YEEDU_RESTAPI_URL}/admin/groups/{group_id}/roles"
            else:
                url = f"{config.YEEDU_RESTAPI_URL}/platform/admin/tenant/{tenant_id}/groups/{group_id}/roles"

            response = requests.request(
                "GET", url, headers=config.header_get, timeout=60, verify=False)
            return response_validator(response)
        except requests.exceptions.RequestException as e:
            logger.exception(f"Failed to connect due to {e}")
            sys.exit(-1)

    def list_group_roles(pageNumber, limit, tenant_id=None):
        try:
            if tenant_id is None:
                url = f"{config.YEEDU_RESTAPI_URL}/admin/roles/groups?pageNumber={pageNumber}&limit={limit}"
            else:
                url = f"{config.YEEDU_RESTAPI_URL}/platform/admin/tenant/{tenant_id}/roles/groups?pageNumber={pageNumber}&limit={limit}"

            response = requests.request(
                "GET", url, headers=config.header_get, timeout=60, verify=False)
            return response_validator(response)
        except requests.exceptions.RequestException as e:
            logger.exception(f"Failed to connect due to {e}")
            sys.exit(-1)

    def get_role_groups(role_id, tenant_id=None):
        try:
            if tenant_id is None:
                url = f"{config.YEEDU_RESTAPI_URL}/admin/roles/groups/{role_id}"
            else:
                url = f"{config.YEEDU_RESTAPI_URL}/platform/admin/tenant/{tenant_id}/roles/groups/{role_id}"

            response = requests.request(
                "GET", url, headers=config.header_get, timeout=60, verify=False)
            return response_validator(response)
        except requests.exceptions.RequestException as e:
            logger.exception(f"Failed to connect due to {e}")
            sys.exit(-1)

    def create_user_role(user_id, role_id, command, tenant_id=None):
        try:
            if command == 'platform-admin':
                if tenant_id is None:
                    url = f"{config.YEEDU_RESTAPI_URL}/platform/admin/tenant/user/{user_id}/role/{role_id}"
                else:
                    url = f"{config.YEEDU_RESTAPI_URL}/platform/admin/tenant/user/{user_id}/role/{role_id}?tenant_id={tenant_id}"
            else:
                url = f"{config.YEEDU_RESTAPI_URL}/admin/user/{user_id}/role/{role_id}"

            response = requests.request(
                "POST", url, headers=config.header_get, timeout=60, verify=False)
            return response_validator(response)
        except requests.exceptions.RequestException as e:
            logger.exception(f"Failed to connect due to {e}")
            sys.exit(-1)

    def delete_user_role(user_id, role_id, command, tenant_id=None):
        try:
            if command == 'platform-admin':
                if tenant_id is None:
                    url = f"{config.YEEDU_RESTAPI_URL}/platform/admin/tenant/user/{user_id}/role/{role_id}"
                else:
                    url = f"{config.YEEDU_RESTAPI_URL}/platform/admin/tenant/user/{user_id}/role/{role_id}?tenant_id={tenant_id}"
            else:
                url = f"{config.YEEDU_RESTAPI_URL}/admin/user/{user_id}/role/{role_id}"

            response = requests.request(
                "DELETE", url, headers=config.header_get, timeout=60, verify=False)
            return response_validator(response)
        except requests.exceptions.RequestException as e:
            logger.exception(f"Failed to connect due to {e}")
            sys.exit(-1)

    def create_group_role(group_id, role_id, command, tenant_id=None):
        try:
            if command == 'platform-admin':
                if tenant_id is None:
                    url = f"{config.YEEDU_RESTAPI_URL}/platform/admin/tenant/group/{group_id}/role/{role_id}"
                else:
                    url = f"{config.YEEDU_RESTAPI_URL}/platform/admin/tenant/group/{group_id}/role/{role_id}?tenant_id={tenant_id}"
            else:
                url = f"{config.YEEDU_RESTAPI_URL}/admin/group/{group_id}/role/{role_id}"

            response = requests.request(
                "POST", url, headers=config.header_get, timeout=60, verify=False)
            return response_validator(response)
        except requests.exceptions.RequestException as e:
            logger.exception(f"Failed to connect due to {e}")
            sys.exit(-1)

    def delete_group_role(group_id, role_id, command, tenant_id=None):
        try:
            if command == 'platform-admin':
                if tenant_id is None:
                    url = f"{config.YEEDU_RESTAPI_URL}/platform/admin/tenant/group/{group_id}/role/{role_id}"
                else:
                    url = f"{config.YEEDU_RESTAPI_URL}/platform/admin/tenant/group/{group_id}/role/{role_id}?tenant_id={tenant_id}"
            else:
                url = f"{config.YEEDU_RESTAPI_URL}/admin/group/{group_id}/role/{role_id}"

            response = requests.request(
                "DELETE", url, headers=config.header_get, timeout=60, verify=False)
            return response_validator(response)
        except requests.exceptions.RequestException as e:
            logger.exception(f"Failed to connect due to {e}")
            sys.exit(-1)
