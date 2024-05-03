from yeeducli.utility.json_utils import response_validator, response_json_custom_order
from yeeducli.utility.logger_utils import Logger
from yeeducli.constants import SPARK_JOB_CONFIG_ORDER
from yeeducli import config
import requests
import sys

logger = Logger.get_logger(__name__, True)


class SparkJobConfig:
    def list_spark_job_config(pageNumber, limit):
        try:
            url = f"{config.YEEDU_RESTAPI_URL}/spark/job/confs?pageNumber={pageNumber}&limit={limit}"

            response = requests.request(
                "GET", url, headers=config.header_get, timeout=60, verify=False)
            if (response.status_code == 200 and (isinstance(response.json(), dict) and response.json().get('data'))):
                unordered_json = response.json()
                unordered_json['data'] = response_json_custom_order(
                    unordered_json.get("data"), SPARK_JOB_CONFIG_ORDER)
                return unordered_json, response.status_code
            else:
                return response_validator(response)
        except requests.exceptions.RequestException as e:
            logger.exception(f"Failed to connect due to {e}")
            sys.exit(-1)

    def add_spark_job_config(json_data):
        try:
            url = f"{config.YEEDU_RESTAPI_URL}/spark/job/conf"

            response = requests.request(
                "POST", url, headers=config.headers, data=json_data, timeout=60, verify=False)
            return response_validator(response)
        except requests.exceptions.RequestException as e:
            logger.exception(f"Failed to connect due to {e}")
            sys.exit(-1)

    def get_spark_job_config_by_id_or_name(job_conf_id=None, job_conf_name=None):
        try:
            if job_conf_id is not None and job_conf_name is not None:
                url = f"{config.YEEDU_RESTAPI_URL}/spark/job/config?job_conf_id={job_conf_id}&job_conf_name={job_conf_name}"
            elif job_conf_id is not None:
                url = f"{config.YEEDU_RESTAPI_URL}/spark/job/conf?job_conf_id={job_conf_id}"
            elif job_conf_name is not None:
                url = f"{config.YEEDU_RESTAPI_URL}/spark/job/conf?job_conf_name={job_conf_name}"
            else:
                url = f"{config.YEEDU_RESTAPI_URL}/spark/job/conf"

            response = requests.request(
                "GET", url, headers=config.header_get, timeout=60, verify=False)
            if (response.status_code == 200 and (isinstance(response.json(), dict) and response.json().get('error') is None)):
                unordered_json = response.json()
                return response_json_custom_order(unordered_json, SPARK_JOB_CONFIG_ORDER), response.status_code
            else:
                return response_validator(response)
        except requests.exceptions.RequestException as e:
            logger.exception(f"Failed to connect due to {e}")
            sys.exit(-1)

    def edit_spark_job_config(json_data, job_conf_id=None, job_conf_name=None):
        try:
            if job_conf_id is not None and job_conf_name is not None:
                url = f"{config.YEEDU_RESTAPI_URL}/spark/job/conf?job_conf_id={job_conf_id}&job_conf_name={job_conf_name}"
            elif job_conf_id is not None:
                url = f"{config.YEEDU_RESTAPI_URL}/spark/job/conf?job_conf_id={job_conf_id}"
            elif job_conf_name is not None:
                url = f"{config.YEEDU_RESTAPI_URL}/spark/job/conf?job_conf_name={job_conf_name}"
            else:
                url = f"{config.YEEDU_RESTAPI_URL}/spark/job/conf"

            response = requests.request(
                "PUT", url, headers=config.headers, data=json_data, timeout=60, verify=False)
            return response_validator(response)
        except requests.exceptions.RequestException as e:
            logger.exception(f"Failed to connect due to {e}")
            sys.exit(-1)

    def delete_spark_job_config_by_id_or_name(job_conf_id=None, job_conf_name=None):
        try:
            if job_conf_id is not None and job_conf_name is not None:
                url = f"{config.YEEDU_RESTAPI_URL}/spark/job/conf?job_conf_id={job_conf_id}&job_conf_name={job_conf_name}"
            elif job_conf_id is not None:
                url = f"{config.YEEDU_RESTAPI_URL}/spark/job/conf?job_conf_id={job_conf_id}"
            elif job_conf_name is not None:
                url = f"{config.YEEDU_RESTAPI_URL}/spark/job/conf?job_conf_name={job_conf_name}"
            else:
                url = f"{config.YEEDU_RESTAPI_URL}/spark/job/conf"

            response = requests.request(
                "DELETE", url, headers=config.header_get, verify=False)
            return response_validator(response)
        except requests.exceptions.RequestException as e:
            logger.exception(f"Failed to connect due to {e}")
            sys.exit(-1)
