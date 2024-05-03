from yeeducli.openapi.cluster.cluster_configuration import ClusterConfiguration
from yeeducli.openapi.cluster.cluster_instance import ClusterInstance
from yeeducli.openapi.cluster.download_cluster_instance_logs import DownloadClusterInstanceLogs
from yeeducli.utility.json_utils import *
from yeeducli.utility.logger_utils import Logger
import json
import sys


# Engine Cluster Configuration
def create_cluster(args):
    try:
        trim_json_data = trim_namespace_json(args)
        json_data = json.dumps(change_output(remove_output(args)))

        response_json, status_code = ClusterConfiguration.add_cluster_config(
            json_data)

        confirm_output(response_json, status_code, trim_json_data)
    except Exception as e:
        logger.exception(e)
        sys.exit(-1)


def get_cluster(args):
    try:
        json_data = change_output(trim_namespace_json(args))

        response_json, status_code = ClusterConfiguration.get_cluster_config_by_id_or_name(
            json_data.get('cluster_conf_id'),
            json_data.get('cluster_conf_name')
        )
        confirm_output(response_json, status_code, json_data)
    except Exception as e:
        logger.exception(e)
        sys.exit(-1)


def list_cluster(args):
    try:
        json_data = change_output(trim_namespace_json(args))

        if (json_data.get("cloud_provider")):
            response_json, status_code = ClusterConfiguration.list_cluster_config(
                json_data.get('page_number'),
                json_data.get('limit'),
                str(json_data.get("cloud_provider")).upper()
            )
            confirm_output(response_json, status_code, json_data)
        else:
            response_json, status_code = ClusterConfiguration.list_cluster_config(
                json_data.get('page_number'),
                json_data.get('limit')
            )
            confirm_output(response_json, status_code, json_data)
    except Exception as e:
        logger.exception(e)
        sys.exit(-1)


def edit_cluster(args):
    try:
        trim_json_data = change_output(trim_namespace_json(args))
        json_data = change_output(remove_output(args))

        if json_data.get('cluster_conf_id'):
            del json_data["cluster_conf_id"]
        if json_data.get('cluster_conf_name'):
            del json_data["cluster_conf_name"]

        json_data = json.dumps(json_data)

        response_json, status_code = ClusterConfiguration.edit_cluster_config(
            json_data,
            trim_json_data.get('cluster_conf_id'),
            trim_json_data.get('cluster_conf_name')
        )
        confirm_output(response_json, status_code, trim_json_data)
    except Exception as e:
        logger.exception(e)
        sys.exit(-1)


# Cluster Instance
def create_instance(args):
    try:
        trim_json_data = trim_namespace_json(args)
        json_data = json.dumps(change_output(remove_output(args)))

        response_json, status_code = ClusterInstance.add_cluster_instance(
            json_data)
        confirm_output(response_json, status_code, trim_json_data)
    except Exception as e:
        logger.exception(e)
        sys.exit(-1)


def list_instance(args):
    try:
        json_data = change_output(trim_namespace_json(args))

        if json_data.get('cluster_status') is None:
            response_json, status_code = ClusterInstance.list_cluster_instance(
                json_data.get('page_number'),
                json_data.get('limit'),
                json_data.get('cluster_conf_id'),
                json_data.get('cluster_conf_name')
            )
        else:
            cluster_status = json_data["cluster_status"].split(
                ",")

            response_json, status_code = ClusterInstance.list_cluster_instance(
                json_data.get('page_number'),
                json_data.get('limit'),
                json_data.get('cluster_conf_id'),
                json_data.get('cluster_conf_name'),
                cluster_status,
            )

        confirm_output(response_json, status_code, json_data)
    except Exception as e:
        logger.exception(e)
        sys.exit(-1)


def get_instance(args):
    try:
        json_data = change_output(trim_namespace_json(args))

        response_json, status_code = ClusterInstance.get_cluster_instance_by_id_or_name(
            json_data.get('cluster_id'),
            json_data.get('cluster_name')
        )
        confirm_output(response_json, status_code, json_data)
    except Exception as e:
        logger.exception(e)
        sys.exit(-1)


def edit_instance(args):
    try:
        trim_json_data = change_output(trim_namespace_json(args))
        json_data = change_output(remove_output(args))

        if json_data.get('cluster_id'):
            del json_data["cluster_id"]
        if json_data.get('cluster_name'):
            del json_data["cluster_name"]

        json_data = json.dumps(json_data)
        response_json, status_code = ClusterInstance.edit_cluster_instance(
            json_data,
            trim_json_data.get('cluster_id'),
            trim_json_data.get('cluster_name')
        )
        confirm_output(response_json, status_code, trim_json_data)
    except Exception as e:
        logger.exception(e)
        sys.exit(-1)


def destroy_instance(args):
    try:
        trim_json_data = change_output(trim_namespace_json(args))

        response_json, status_code = ClusterInstance.destroy_cluster_instance_by_id_or_name(
            trim_json_data.get('cluster_id'),
            trim_json_data.get('cluster_name')
        )
        confirm_output(response_json, status_code, trim_json_data)
    except Exception as e:
        logger.exception(e)
        sys.exit(-1)


def uptime_instance(args):
    try:
        trim_json_data = change_output(trim_namespace_json(args))

        response_json, status_code = ClusterInstance.uptime_cluster_instance_by_id_or_name(
            trim_json_data.get('cluster_id'),
            trim_json_data.get('cluster_name')
        )
        confirm_output(response_json, status_code, trim_json_data)
    except Exception as e:
        logger.exception(e)
        sys.exit(-1)


def start_instance(args):
    try:
        trim_json_data = change_output(trim_namespace_json(args))

        response_json, status_code = ClusterInstance.start_cluster_instance_by_id_or_name(
            trim_json_data.get('cluster_id'),
            trim_json_data.get('cluster_name')
        )
        confirm_output(response_json, status_code, trim_json_data)
    except Exception as e:
        logger.exception(e)
        sys.exit(-1)


def stop_instance(args):
    try:
        trim_json_data = change_output(trim_namespace_json(args))

        response_json, status_code = ClusterInstance.stop_cluster_instance_by_id_or_name(
            trim_json_data.get('cluster_id'),
            trim_json_data.get('cluster_name')
        )
        confirm_output(response_json, status_code, trim_json_data)
    except Exception as e:
        logger.exception(e)
        sys.exit(-1)


# Download Cluster Instance Log Files
def download_cluster_instance_log_records(args):
    try:
        json_data = change_output(trim_namespace_json(args))

        response_json, status_code = DownloadClusterInstanceLogs.get_cluster_instance_log_records(
            json_data.get('log_type'),
            json_data.get('cluster_id'),
            json_data.get('cluster_name')
        )
        if (response_json is not True):
            confirm_output(response_json, status_code, json_data)
    except Exception as e:
        logger.exception(e)
        sys.exit(-1)


# Get Spark Job Statistics of an Cluster Instance
def get_instance_job_stats(args):
    try:
        json_data = change_output(trim_namespace_json(args))

        response_json, status_code = ClusterInstance.get_job_stats_by_cluster_instance_id_or_name(
            json_data.get('cluster_id'),
            json_data.get('cluster_name')
        )
        confirm_output(response_json, status_code, json_data)
    except Exception as e:
        logger.exception(e)
        sys.exit(-1)
