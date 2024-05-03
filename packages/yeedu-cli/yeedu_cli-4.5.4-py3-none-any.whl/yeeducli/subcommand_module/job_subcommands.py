from yeeducli.openapi.job.spark_job_config import SparkJobConfig
from yeeducli.openapi.job.spark_job_instance import SparkJobInstance
from yeeducli.openapi.job.download_job_instance_logs import DownloadJobInstanceLogs
from yeeducli.utility.logger_utils import Logger
from yeeducli.utility.json_utils import *
import json
import sys

logger = Logger.get_logger(__name__, True)


# Spark Job Configuration
def create_spark_job_config(args):
    try:
        trim_json_data = trim_namespace_json(args)
        json_data = change_output(remove_output(args))

        if hasattr(args, 'raw_scala_code') and trim_json_data.get('raw_scala_code')[0] != None:
            rawScalaCodeFilePath = checkFilePathExists(
                trim_json_data.get('raw_scala_code')[0], 'raw_scala_code')

            json_data['rawScalaCode'] = readFileContent(rawScalaCodeFilePath)

            del json_data["raw_scala_code"]
            response_json, status_code = SparkJobConfig.add_spark_job_config(
                json.dumps(json_data))
            confirm_output(response_json, status_code, trim_json_data)

        else:
            response_json, status_code = SparkJobConfig.add_spark_job_config(
                json.dumps(json_data))
            confirm_output(response_json, status_code, trim_json_data)
    except Exception as e:
        logger.exception(e)
        sys.exit(-1)


def describe_spark_job_config(args):
    try:
        json_data = change_output(trim_namespace_json(args))

        response_json, status_code = SparkJobConfig.get_spark_job_config_by_id_or_name(
            json_data.get('job_conf_id'),
            json_data.get('job_conf_name')
        )
        confirm_output(response_json, status_code, json_data)
    except Exception as e:
        logger.exception(e)
        sys.exit(-1)


def list_spark_job_config(args):
    try:
        json_data = change_output(trim_namespace_json(args))

        response_json, status_code = SparkJobConfig.list_spark_job_config(
            json_data.get('page_number'),
            json_data.get('limit')
        )
        confirm_output(response_json, status_code, json_data)
    except Exception as e:
        logger.exception(e)
        sys.exit(-1)


def edit_spark_job_config(args):
    try:
        trim_json_data = change_output(trim_namespace_json(args))
        json_data = change_output(remove_output(args))

        if json_data.get('job_conf_id') is not None:
            del json_data["job_conf_id"]
        if json_data.get('job_conf_name') is not None:
            del json_data["job_conf_name"]

        if hasattr(args, 'raw_scala_code') and trim_json_data.get('raw_scala_code') != None:
            rawScalaCodeFilePath = checkFilePathExists(
                trim_json_data.get('raw_scala_code'), 'raw_scala_code')

            json_data['rawScalaCode'] = readFileContent(rawScalaCodeFilePath)

            del json_data["raw_scala_code"]
            response_json, status_code = SparkJobConfig.edit_spark_job_config(
                json.dumps(json_data),
                trim_json_data.get('job_conf_id'),
                trim_json_data.get('job_conf_name')
            )
            confirm_output(response_json, status_code, trim_json_data)

        else:
            response_json, status_code = SparkJobConfig.edit_spark_job_config(
                json.dumps(json_data),
                trim_json_data.get('job_conf_id'),
                trim_json_data.get('job_conf_name')
            )
            confirm_output(response_json, status_code, trim_json_data)
    except Exception as e:
        logger.exception(e)
        sys.exit(-1)


def delete_spark_job_config(args):
    try:
        trim_json_data = change_output(trim_namespace_json(args))

        response_json, status_code = SparkJobConfig.delete_spark_job_config_by_id_or_name(
            trim_json_data.get('job_conf_id'),
            trim_json_data.get('job_conf_name')
        )
        confirm_output(response_json, status_code, trim_json_data)
    except Exception as e:
        logger.exception(e)
        sys.exit(-1)


# Spark Job Instance
def start_spark_job_run(args):
    try:
        trim_json_data = trim_namespace_json(args)
        json_data = change_output(remove_output(args))

        response_json, status_code = SparkJobInstance.add_spark_job_instance(
            json_data)
        confirm_output(response_json, status_code, trim_json_data)
    except Exception as e:
        logger.exception(e)
        sys.exit(-1)


def describe_spark_job_inst(args):
    try:
        json_data = trim_namespace_json(args)

        response_json, status_code = SparkJobInstance.get_spark_job_inst_by_id(
            json_data.get('job_id')[0])
        confirm_output(response_json, status_code, json_data)
    except Exception as e:
        logger.exception(e)
        sys.exit(-1)


def list_spark_job_inst(args):
    try:
        json_data = change_output(trim_namespace_json(args))

        if json_data.get('job_status') is not None:

            response_json, status_code = SparkJobInstance.list_spark_job_instances(
                json_data.get('page_number'),
                json_data.get('limit'),
                json_data.get('cluster_id'),
                json_data.get('job_conf_id'),
                json_data.get('job_conf_name'),
                json_data.get('job_status').upper()
            )

            confirm_output(response_json, status_code, json_data)

        else:
            response_json, status_code = SparkJobInstance.list_spark_job_instances(
                json_data.get('page_number'),
                json_data.get('limit'),
                json_data.get('cluster_id'),
                json_data.get('job_conf_id'),
                json_data.get('job_conf_name')
            )

            confirm_output(response_json, status_code, json_data)

    except Exception as e:
        logger.exception(e)
        sys.exit(-1)


def kill_spark_job_inst(args):
    try:
        trim_json_data = trim_namespace_json(args)
        response_json, status_code = SparkJobInstance.kill_spark_job_instance_by_id(
            trim_json_data.get('job_id')[0])
        confirm_output(response_json, status_code, trim_json_data)
    except Exception as e:
        logger.exception(e)
        sys.exit(-1)


def get_workflow_job_instance_details(args):
    try:
        json_data = trim_namespace_json(args)

        response_json, status_code = SparkJobInstance.get_workflow_job_instance_details_by_appId(
            json_data.get('job_application_id')[0])
        confirm_output(response_json, status_code, json_data)
    except Exception as e:
        logger.exception(e)
        sys.exit(-1)


# Download Job Instance Log Files
def download_job_instance_log_records(args):
    try:
        json_data = change_output(trim_namespace_json(args))

        response_json, status_code = DownloadJobInstanceLogs.get_job_instance_log_records(
            json_data.get('job_id'),
            json_data.get('log_type')
        )
        if (response_json is not True):
            confirm_output(response_json, status_code, json_data)

    except Exception as e:
        logger.exception(e)
        sys.exit(-1)
