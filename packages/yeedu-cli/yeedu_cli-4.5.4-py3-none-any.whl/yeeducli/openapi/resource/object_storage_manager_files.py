from yeeducli.utility.json_utils import response_validator, response_json_custom_order
from yeeducli.utility.logger_utils import Logger
from yeeducli.constants import OBJECT_STORAGE_MANAGER_FILES_ORDER
from yeeducli import config
import requests
import sys
import os
import urllib.parse

logger = Logger.get_logger(__name__, True)


class ObjectStorageManagerFiles:
    def get_object_storage_manager_files_by_object_storage_manager_id(object_storage_manager_id=None, file_id=None):
        try:
            if (object_storage_manager_id != None and file_id == None):
                url = f"{config.YEEDU_RESTAPI_URL}/object_storage_manager/{object_storage_manager_id}/files"
            elif (object_storage_manager_id != None and file_id != None):
                url = f"{config.YEEDU_RESTAPI_URL}/object_storage_manager/{object_storage_manager_id}/files/{file_id}"

            response = requests.request(
                "GET", url, headers=config.header_get, timeout=200, verify=False)

            if (response.status_code == 200 and (isinstance(response.json(), list) or (isinstance(response.json(), dict) and response.json().get('error') is None))):
                unordered_json = response.json()
                return response_json_custom_order(unordered_json, OBJECT_STORAGE_MANAGER_FILES_ORDER), response.status_code
            else:
                return response_validator(response)
        except requests.exceptions.RequestException as e:
            logger.exception(f"Failed to connect due to {e}")
            sys.exit(-1)

    def add_object_storage_manager_files(object_storage_manager_id, local_file_path, preserve_path, overwrite):
        try:
            url = f"{config.YEEDU_RESTAPI_URL}/object_storage_manager/{object_storage_manager_id}/files?preserve_path={preserve_path}&overwrite={overwrite}"

            files = {
                'fileObject': open(local_file_path, 'rb')
            }

            if preserve_path:
                url = f"{config.YEEDU_RESTAPI_URL}/object_storage_manager/{object_storage_manager_id}/files?local_file_path={urllib.parse.quote(os.path.split(local_file_path)[0],safe='')}&preserve_path={preserve_path}&overwrite={overwrite}"

            response = requests.request(
                "POST", url, headers=config.headers_files, files=files, verify=False)

            return response_validator(response)
        except requests.exceptions.RequestException as e:
            logger.exception(f"Failed to connect due to {e}")
            sys.exit(-1)

    def delete_object_storage_manager_file(object_storage_manager_id, file_id):
        try:
            url = f"{config.YEEDU_RESTAPI_URL}/object_storage_manager/{object_storage_manager_id}/files/{file_id}"

            response = requests.request(
                "DELETE", url, headers=config.header_get, verify=False)

            return response_validator(response)
        except requests.exceptions.RequestException as e:
            logger.exception(f"Failed to connect due to {e}")
            sys.exit(-1)
