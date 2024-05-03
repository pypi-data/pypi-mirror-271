from yeeducli.utility.json_utils import response_validator
from yeeducli.utility.logger_utils import Logger
from yeeducli import config
import requests
import sys
import json

logger = Logger.get_logger(__name__, True)


class SparkJobInstance:

    def list_spark_job_instances(page_number, limit, cluster_id, job_conf_id=None, job_conf_name=None, job_status=None):
        try:
            # | 1 | 1 | 1 |
            if job_conf_id is not None and job_conf_name is not None and job_status is not None:
                url = f"{config.YEEDU_RESTAPI_URL}/spark/jobs?cluster_id={cluster_id}&job_conf_id={job_conf_id}&job_conf_name={job_conf_name}&job_status={job_status}&pageNumber={page_number}&limit={limit}"

            # | 1 | 1 | 0 |
            elif job_conf_id is not None and job_conf_name is not None and job_status is None:
                url = f"{config.YEEDU_RESTAPI_URL}/spark/jobs?cluster_id={cluster_id}&job_conf_id={job_conf_id}&job_conf_name={job_conf_name}&pageNumber={page_number}&limit={limit}"

            # | 1 | 0 | 0 |
            elif job_conf_id is not None and job_conf_name is None and job_status is None:
                url = f"{config.YEEDU_RESTAPI_URL}/spark/jobs?cluster_id={cluster_id}&job_conf_id={job_conf_id}&pageNumber={page_number}&limit={limit}"

            # | 0 | 1 | 0 |
            elif job_conf_id is None and job_conf_name is not None and job_status is None:
                url = f"{config.YEEDU_RESTAPI_URL}/spark/jobs?cluster_id={cluster_id}&job_conf_name={job_conf_name}&pageNumber={page_number}&limit={limit}"

            # | 0 | 0 | 1 |
            elif job_conf_id is None and job_conf_name is None and job_status is not None:
                url = f"{config.YEEDU_RESTAPI_URL}/spark/jobs?cluster_id={cluster_id}&job_status={job_status}&pageNumber={page_number}&limit={limit}"

            # | 0 | 1 | 1 |
            elif job_conf_id is None and job_conf_name is not None and job_status is not None:
                url = f"{config.YEEDU_RESTAPI_URL}/spark/jobs?cluster_id={cluster_id}&job_conf_name={job_conf_name}&job_status={job_status}&pageNumber={page_number}&limit={limit}"

            # | 1 | 0 | 1 |
            elif job_conf_id is not None and job_conf_name is None and job_status is not None:
                url = f"{config.YEEDU_RESTAPI_URL}/spark/jobs?cluster_id={cluster_id}&job_conf_id={job_conf_id}&job_status={job_status}&pageNumber={page_number}&limit={limit}"

            # | 0 | 0 | 0 |
            elif job_conf_id is None and job_conf_name is None and job_status is None:
                url = f"{config.YEEDU_RESTAPI_URL}/spark/jobs?cluster_id={cluster_id}&pageNumber={page_number}&limit={limit}"

            response = requests.request(
                "GET", url, headers=config.header_get, timeout=200, verify=False)
            return response_validator(response)

        except requests.exceptions.RequestException as e:
            logger.exception(f"Failed to connect due to {e}")
            sys.exit(-1)

    def add_spark_job_instance(json_data):
        try:
            url = f"{config.YEEDU_RESTAPI_URL}/spark/job"
            response = requests.request(
                "POST", url, headers=config.headers, data=json.dumps(json_data), timeout=60, verify=False)
            return response_validator(response)
        except requests.exceptions.RequestException as e:
            logger.exception(f"Failed to connect due to {e}")
            sys.exit(-1)

    def get_spark_job_inst_by_id(job_id):
        try:
            url = f"{config.YEEDU_RESTAPI_URL}/spark/job/{job_id}"

            response = requests.request(
                "GET", url, headers=config.header_get, timeout=60, verify=False)
            return response_validator(response)
        except requests.exceptions.RequestException as e:
            logger.exception(f"Failed to connect due to {e}")
            sys.exit(-1)

    def kill_spark_job_instance_by_id(job_id):
        try:
            url = f"{config.YEEDU_RESTAPI_URL}/spark/job/kill/{job_id}"

            response = requests.request(
                "POST", url, headers=config.header_get, verify=False)
            return response_validator(response)
        except requests.exceptions.RequestException as e:
            logger.exception(f"Failed to connect due to {e}")
            sys.exit(-1)

    def get_workflow_job_instance_details_by_appId(job_application_id):
        try:
            url = f"{config.YEEDU_RESTAPI_URL}/spark/job/workflow_job_instance_details/{job_application_id}"

            response = requests.request(
                "GET", url, headers=config.header_get, timeout=60, verify=False)
            return response_validator(response)
        except requests.exceptions.RequestException as e:
            logger.exception(f"Failed to connect due to {e}")
            sys.exit(-1)
