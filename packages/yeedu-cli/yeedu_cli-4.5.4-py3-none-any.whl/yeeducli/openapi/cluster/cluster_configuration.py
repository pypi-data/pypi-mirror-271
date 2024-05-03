from yeeducli.utility.json_utils import response_validator, response_json_custom_order
from yeeducli.utility.logger_utils import Logger
from yeeducli.constants import ENGINE_CLUSTER_CONFIG_ORDER
from yeeducli import config
import requests
import sys

logger = Logger.get_logger(__name__, True)


class ClusterConfiguration:
    def list_cluster_config(pageNumber, limit, cloud_provider=None):
        try:
            if cloud_provider == None:
                url = f"{config.YEEDU_RESTAPI_URL}/cluster/confs?pageNumber={pageNumber}&limit={limit}"
            else:
                url = f"{config.YEEDU_RESTAPI_URL}/cluster/confs?cloud_provider={cloud_provider}&pageNumber={pageNumber}&limit={limit}"

            response = requests.request(
                "GET", url, headers=config.header_get, timeout=60, verify=False)
            if (response.status_code == 200 and (isinstance(response.json(), dict) and response.json().get('data'))):
                unordered_json = response.json()
                unordered_json['data'] = response_json_custom_order(
                    unordered_json.get("data"), ENGINE_CLUSTER_CONFIG_ORDER)
                return unordered_json, response.status_code
            else:
                return response_validator(response)
        except requests.exceptions.RequestException as e:
            logger.exception(f"Failed to connect due to {e}")
            sys.exit(-1)

    def add_cluster_config(json_data):
        try:
            url = f"{config.YEEDU_RESTAPI_URL}/cluster/conf"

            response = requests.request(
                "POST", url, headers=config.headers, data=json_data, timeout=60, verify=False)
            return response_validator(response)
        except requests.exceptions.RequestException as e:
            logger.exception(f"Failed to connect due to {e}")
            sys.exit(-1)

    def get_cluster_config_by_id_or_name(cluster_conf_id=None, cluster_conf_name=None):
        try:
            if cluster_conf_id is not None and cluster_conf_name is not None:
                url = f"{config.YEEDU_RESTAPI_URL}/cluster/conf?cluster_conf_id={cluster_conf_id}&cluster_conf_name={cluster_conf_name}"
            elif cluster_conf_name is not None:
                url = f"{config.YEEDU_RESTAPI_URL}/cluster/conf?cluster_conf_name={cluster_conf_name}"
            elif cluster_conf_id is not None:
                url = f"{config.YEEDU_RESTAPI_URL}/cluster/conf?cluster_conf_id={cluster_conf_id}"
            else:
                url = f"{config.YEEDU_RESTAPI_URL}/cluster/conf"

            response = requests.request(
                "GET", url, headers=config.header_get, timeout=60, verify=False)
            if (response.status_code == 200 and (isinstance(response.json(), dict) and response.json().get('error') is None)):
                unordered_json = response.json()
                return response_json_custom_order(unordered_json, ENGINE_CLUSTER_CONFIG_ORDER), response.status_code
            else:
                return response_validator(response)
        except requests.exceptions.RequestException as e:
            logger.exception(f"Failed to connect due to {e}")
            sys.exit(-1)

    def edit_cluster_config(json_data, cluster_conf_id=None, cluster_conf_name=None):
        try:
            if cluster_conf_id is not None and cluster_conf_name is not None:
                url = f"{config.YEEDU_RESTAPI_URL}/cluster/conf?cluster_conf_id={cluster_conf_id}&cluster_conf_name={cluster_conf_name}"
            elif cluster_conf_name is not None:
                url = f"{config.YEEDU_RESTAPI_URL}/cluster/conf?cluster_conf_name={cluster_conf_name}"
            elif cluster_conf_id is not None:
                url = f"{config.YEEDU_RESTAPI_URL}/cluster/conf?cluster_conf_id={cluster_conf_id}"
            else:
                url = f"{config.YEEDU_RESTAPI_URL}/cluster/conf"

            response = requests.request(
                "PUT", url, headers=config.headers, data=json_data, timeout=60, verify=False)
            return response_validator(response)
        except requests.exceptions.RequestException as e:
            logger.exception(f"Failed to connect due to {e}")
            sys.exit(-1)
