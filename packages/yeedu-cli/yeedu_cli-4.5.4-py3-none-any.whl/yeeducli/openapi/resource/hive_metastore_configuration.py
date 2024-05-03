from yeeducli.utility.json_utils import response_validator
from yeeducli.utility.logger_utils import Logger
from yeeducli import config
import requests
import sys

logger = Logger.get_logger(__name__, True)


class HiveMetastoreConfiguration:

    def add_hive_metastore_configuration(json_data):
        try:
            url = f"{config.YEEDU_RESTAPI_URL}/hive_metastore_config"

            response = requests.request(
                "POST", url, headers=config.headers, json=json_data, verify=False)

            return response_validator(response)

        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to connect due to {e}")
            sys.exit(-1)

    def list_hive_metastore_config():

        url = f"{config.YEEDU_RESTAPI_URL}/hive_metastore_config"
        try:
            response = requests.request(
                "GET", url, headers=config.header_get, verify=False)

            return response_validator(response)
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to connect due to {e}")
            sys.exit(-1)

    def get_hive_metastore_config_by_id(hive_metastore_conf_id):
        url = f"{config.YEEDU_RESTAPI_URL}/hive_metastore_config/{hive_metastore_conf_id}"
        try:
            response = requests.request(
                "GET", url, headers=config.header_get, verify=False)

            return response_validator(response)
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to connect due to {e}")
            sys.exit(-1)

    def edit_hive_metastore_config(hive_metastore_conf_id, json_data):
        try:
            url = f"{config.YEEDU_RESTAPI_URL}/hive_metastore_config/{hive_metastore_conf_id}"

            response = requests.request(
                "PUT", url, headers=config.headers, json=json_data, verify=False)

            return response_validator(response)
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to connect due to {e}")
            sys.exit(-1)

    def delete_hive_metastore_config_by_id(hive_metastore_conf_id):
        url = f"{config.YEEDU_RESTAPI_URL}/hive_metastore_config/{hive_metastore_conf_id}"
        try:
            response = requests.request(
                "DELETE", url, headers=config.header_get, verify=False)
            return response_validator(response)
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to connect due to {e}")
            sys.exit(-1)
