from yeeducli.utility.json_utils import response_validator, prepareQueryParamsForTypeArray
from yeeducli.utility.logger_utils import Logger
from yeeducli import config
import requests
import sys

logger = Logger.get_logger(__name__, True)


class ClusterInstance:
    def list_cluster_instance(pageNumber, limit, cluster_conf_id=None, cluster_conf_name=None, cluster_status=None):
        try:
            # | 1 | 1 | 1 |
            if cluster_conf_id is not None and cluster_conf_name is not None and cluster_status is not None:

                queryParameters = prepareQueryParamsForTypeArray(
                    cluster_status, pageNumber, limit)

                url = f"{config.YEEDU_RESTAPI_URL}/clusters?{queryParameters}&cluster_conf_id={cluster_conf_id}&cluster_conf_name={cluster_conf_name}"

            # | 1 | 1 | 0 |
            elif cluster_conf_id is not None and cluster_conf_name is not None and cluster_status is None:
                url = f"{config.YEEDU_RESTAPI_URL}/clusters?cluster_conf_id={cluster_conf_id}&cluster_conf_name={cluster_conf_name}&pageNumber={pageNumber}&limit={limit}"

            # | 1 | 0 | 0 |
            elif cluster_conf_id is not None and cluster_conf_name is None and cluster_status is None:
                url = f"{config.YEEDU_RESTAPI_URL}/clusters?cluster_conf_id={cluster_conf_id}&pageNumber={pageNumber}&limit={limit}"

            # | 0 | 1 | 0 |
            elif cluster_conf_id is None and cluster_conf_name is not None and cluster_status is None:
                url = f"{config.YEEDU_RESTAPI_URL}/clusters?cluster_conf_name={cluster_conf_name}&pageNumber={pageNumber}&limit={limit}"

            # | 0 | 0 | 1 |
            elif cluster_conf_id is None and cluster_conf_name is None and cluster_status is not None:

                queryParameters = prepareQueryParamsForTypeArray(
                    cluster_status, pageNumber, limit)

                url = f"{config.YEEDU_RESTAPI_URL}/clusters?{queryParameters}"

            # | 0 | 1 | 1 |
            elif cluster_conf_id is None and cluster_conf_name is not None and cluster_status is not None:

                queryParameters = prepareQueryParamsForTypeArray(
                    cluster_status, pageNumber, limit)

                url = f"{config.YEEDU_RESTAPI_URL}/clusters?{queryParameters}&cluster_conf_name={cluster_conf_name}"

            # | 1 | 0 | 1 |
            elif cluster_conf_id is not None and cluster_conf_name is None and cluster_status is not None:

                queryParameters = prepareQueryParamsForTypeArray(
                    cluster_status, pageNumber, limit)

                url = f"{config.YEEDU_RESTAPI_URL}/clusters?{queryParameters}&cluster_conf_id={cluster_conf_id}"

            # | 0 | 0 | 0 |
            elif cluster_conf_id is None and cluster_conf_name is None and cluster_status is None:
                url = f"{config.YEEDU_RESTAPI_URL}/clusters?pageNumber={pageNumber}&limit={limit}"

            response = requests.request(
                "GET", url, headers=config.header_get, verify=False)
            return response_validator(response)

        except requests.exceptions.RequestException as e:
            logger.exception(f"Failed to connect due to {e}")
            sys.exit(-1)

    def add_cluster_instance(json_data):
        try:
            url = f"{config.YEEDU_RESTAPI_URL}/cluster"
            response = requests.request(
                "POST", url, headers=config.headers, data=json_data, timeout=60, verify=False)
            return response_validator(response)
        except requests.exceptions.RequestException as e:
            logger.exception(f"Failed to connect due to {e}")
            sys.exit(-1)

    def get_cluster_instance_by_id_or_name(cluster_id=None, cluster_name=None):
        try:
            if cluster_id is not None and cluster_name is not None:
                url = f"{config.YEEDU_RESTAPI_URL}/cluster?cluster_id={cluster_id}&cluster_name={cluster_name}"
            elif cluster_name is not None:
                url = f"{config.YEEDU_RESTAPI_URL}/cluster?cluster_name={cluster_name}"
            elif cluster_id is not None:
                url = f"{config.YEEDU_RESTAPI_URL}/cluster?cluster_id={cluster_id}"
            else:
                url = f"{config.YEEDU_RESTAPI_URL}/cluster"

            response = requests.request(
                "GET", url, headers=config.header_get, timeout=60, verify=False)
            return response_validator(response)
        except requests.exceptions.RequestException as e:
            logger.exception(f"Failed to connect due to {e}")
            sys.exit(-1)

    def edit_cluster_instance(json_data, cluster_id=None, cluster_name=None):
        try:
            if cluster_id is not None and cluster_name is not None:
                url = f"{config.YEEDU_RESTAPI_URL}/cluster?cluster_id={cluster_id}&cluster_name={cluster_name}"
            elif cluster_name is not None:
                url = f"{config.YEEDU_RESTAPI_URL}/cluster?cluster_name={cluster_name}"
            elif cluster_id is not None:
                url = f"{config.YEEDU_RESTAPI_URL}/cluster?cluster_id={cluster_id}"
            else:
                url = f"{config.YEEDU_RESTAPI_URL}/cluster"

            response = requests.request(
                "PUT", url, headers=config.headers, data=json_data, timeout=60, verify=False)
            return response_validator(response)
        except requests.exceptions.RequestException as e:
            logger.exception(f"Failed to connect due to {e}")
            sys.exit(-1)

    def destroy_cluster_instance_by_id_or_name(cluster_id=None, cluster_name=None):
        try:
            url = f"{config.YEEDU_RESTAPI_URL}/cluster/destroy"

            request_body = {}

            if cluster_id is not None and cluster_name is not None:
                request_body = {
                    "cluster_id": cluster_id,
                    "cluster_name": cluster_name
                }
            elif cluster_name is not None:
                request_body = {
                    "cluster_name": cluster_name
                }
            elif cluster_id is not None:
                request_body = {
                    "cluster_id": cluster_id
                }

            response = requests.request(
                "POST", url, json=request_body, headers=config.headers, verify=False)
            return response_validator(response)
        except requests.exceptions.RequestException as e:
            logger.exception(f"Failed to connect due to {e}")
            sys.exit(-1)

    def uptime_cluster_instance_by_id_or_name(cluster_id=None, cluster_name=None):
        try:
            url = f"{config.YEEDU_RESTAPI_URL}/cluster/uptime"

            request_body = {}

            if cluster_id is not None and cluster_name is not None:
                request_body = {
                    "cluster_id": cluster_id,
                    "cluster_name": cluster_name
                }
            elif cluster_name is not None:
                request_body = {
                    "cluster_name": cluster_name
                }
            elif cluster_id is not None:
                request_body = {
                    "cluster_id": cluster_id
                }

            response = requests.request(
                "POST", url, json=request_body, headers=config.headers, verify=False)
            return response_validator(response)
        except requests.exceptions.RequestException as e:
            logger.exception(f"Failed to connect due to {e}")
            sys.exit(-1)

    def start_cluster_instance_by_id_or_name(cluster_id=None, cluster_name=None):
        try:
            url = f"{config.YEEDU_RESTAPI_URL}/cluster/start"

            request_body = {}

            if cluster_id is not None and cluster_name is not None:
                request_body = {
                    "cluster_id": cluster_id,
                    "cluster_name": cluster_name
                }
            elif cluster_name is not None:
                request_body = {
                    "cluster_name": cluster_name
                }
            elif cluster_id is not None:
                request_body = {
                    "cluster_id": cluster_id
                }

            response = requests.request(
                "POST", url, json=request_body, headers=config.headers, verify=False)
            return response_validator(response)
        except requests.exceptions.RequestException as e:
            logger.exception(f"Failed to connect due to {e}")
            sys.exit(-1)

    def stop_cluster_instance_by_id_or_name(cluster_id=None, cluster_name=None):
        try:
            url = f"{config.YEEDU_RESTAPI_URL}/cluster/stop"

            request_body = {}

            if cluster_id is not None and cluster_name is not None:
                request_body = {
                    "cluster_id": cluster_id,
                    "cluster_name": cluster_name
                }
            elif cluster_name is not None:
                request_body = {
                    "cluster_name": cluster_name
                }
            elif cluster_id is not None:
                request_body = {
                    "cluster_id": cluster_id
                }

            response = requests.request(
                "POST", url, json=request_body, headers=config.headers, verify=False)
            return response_validator(response)
        except requests.exceptions.RequestException as e:
            logger.exception(f"Failed to connect due to {e}")
            sys.exit(-1)

    def get_job_stats_by_cluster_instance_id_or_name(cluster_id=None, cluster_name=None):
        try:
            if cluster_id is not None and cluster_name is not None:
                url = f"{config.YEEDU_RESTAPI_URL}/cluster/stats?cluster_id={cluster_id}&cluster_name={cluster_name}"
            elif cluster_name is not None:
                url = f"{config.YEEDU_RESTAPI_URL}/cluster/stats?cluster_name={cluster_name}"
            elif cluster_id is not None:
                url = f"{config.YEEDU_RESTAPI_URL}/cluster/stats?cluster_id={cluster_id}"
            else:
                url = f"{config.YEEDU_RESTAPI_URL}/cluster/stats"

            response = requests.request(
                "GET", url, headers=config.header_get, timeout=60, verify=False)
            return response_validator(response)
        except requests.exceptions.RequestException as e:
            logger.exception(f"Failed to connect due to {e}")
            sys.exit(-1)
