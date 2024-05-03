from yeeducli.openapi.resource.boot_disk_image_configuration import BootDiskImageConfiguration
from yeeducli.openapi.resource.volume_configuration import VolumeConfiguration
from yeeducli.openapi.resource.network_configuration import NetworkConfiguration
from yeeducli.openapi.resource.machine_configuration import MachineConfiguration
from yeeducli.openapi.resource.credentials_config import CredentialsConfig
from yeeducli.openapi.resource.object_storage_manager import ObjectStorageManager
from yeeducli.openapi.resource.object_storage_manager_files import ObjectStorageManagerFiles
from yeeducli.openapi.resource.hive_metastore_configuration import HiveMetastoreConfiguration
from yeeducli.openapi.resource.lookup import Lookup
from yeeducli.utility.json_utils import *
from yeeducli.utility.logger_utils import Logger
import json
import sys

logger = Logger.get_logger(__name__, True)


# Cloud Provider
def list_providers(args):
    try:
        json_data = trim_namespace_json(args)
        response_json, status_code = Lookup.get_providers()
        confirm_output(response_json, status_code, json_data)
    except Exception as e:
        logger.exception(e)
        sys.exit(-1)


def describe_provider(args):
    try:
        json_data = trim_namespace_json(args)
        response_json, status_code = Lookup.get_provider_by_id(
            json_data.get('cloud_provider_id')[0])
        confirm_output(response_json, status_code, json_data)
    except Exception as e:
        logger.exception(e)
        sys.exit(-1)


def list_az_by_provider_id(args):
    try:
        json_data = trim_namespace_json(args)

        response_json, status_code = Lookup.get_az_by_provider_id(
            json_data.get('cloud_provider_id')[0])
        confirm_output(response_json, status_code, json_data)
    except Exception as e:
        logger.exception(e)
        sys.exit(-1)


def describe_az_by_provider_id_and_zone_id(args):
    try:
        json_data = trim_namespace_json(args)

        response_json, status_code = Lookup.get_az_by_provider_id_and_zone_id(
            json_data.get('cloud_provider_id')[0], json_data.get('availability_zone_id')[0])
        confirm_output(response_json, status_code, json_data)
    except Exception as e:
        logger.exception(e)
        sys.exit(-1)


def list_machine_type_by_provider_id(args):
    try:
        json_data = trim_namespace_json(args)

        response_json, status_code = Lookup.get_machine_type_by_provider_id(
            json_data.get('cloud_provider_id')[0])
        confirm_output(response_json, status_code, json_data)
    except Exception as e:
        logger.exception(e)
        sys.exit(-1)


def describe_machine_type_by_provider_id_and_machine_type_id(args):
    try:
        json_data = trim_namespace_json(args)

        response_json, status_code = Lookup.get_machine_type_by_provider_id_and_machine_type_id(
            json_data.get('cloud_provider_id')[0], json_data.get("machine_type_id")[0])
        confirm_output(response_json, status_code, json_data)
    except Exception as e:
        logger.exception(e)
        sys.exit(-1)


def list_disk_machine_types(args):
    try:
        json_data = trim_namespace_json(args)
        response_json, status_code = Lookup.get_disk_machine_type()
        confirm_output(response_json, status_code, json_data)
    except Exception as e:
        logger.exception(e)
        sys.exit(-1)


def list_credential_types(args):
    try:
        json_data = trim_namespace_json(args)
        response_json, status_code = Lookup.get_credential_type()
        confirm_output(response_json, status_code, json_data)
    except Exception as e:
        logger.exception(e)
        sys.exit(-1)


def list_lookup_engine_cluster_instance_status(args):
    try:
        json_data = trim_namespace_json(args)
        response_json, status_code = Lookup.get_lookup_engine_cluster_instance_status()
        confirm_output(response_json, status_code, json_data)
    except Exception as e:
        logger.exception(e)
        sys.exit(-1)


def list_lookup_spark_compute_type(args):
    try:
        json_data = trim_namespace_json(args)
        response_json, status_code = Lookup.get_lookup_spark_compute_type()
        confirm_output(response_json, status_code, json_data)
    except Exception as e:
        logger.exception(e)
        sys.exit(-1)


def list_lookup_spark_infra_version(args):
    try:
        json_data = trim_namespace_json(args)
        response_json, status_code = Lookup.get_lookup_spark_infra_version()
        confirm_output(response_json, status_code, json_data)
    except Exception as e:
        logger.exception(e)
        sys.exit(-1)


def list_lookup_spark_job_status(args):
    try:
        json_data = trim_namespace_json(args)
        response_json, status_code = Lookup.get_lookup_spark_job_status()
        confirm_output(response_json, status_code, json_data)
    except Exception as e:
        logger.exception(e)
        sys.exit(-1)


def list_lookup_workflow_execution_state(args):
    try:
        json_data = trim_namespace_json(args)
        response_json, status_code = Lookup.get_lookup_workflow_execution_state()
        confirm_output(response_json, status_code, json_data)
    except Exception as e:
        logger.exception(e)
        sys.exit(-1)


def list_lookup_workflow_type(args):
    try:
        json_data = trim_namespace_json(args)
        response_json, status_code = Lookup.get_lookup_workflow_type()
        confirm_output(response_json, status_code, json_data)
    except Exception as e:
        logger.exception(e)
        sys.exit(-1)


# Volume Configuration
def create_volume(args):
    try:
        trim_json_data = trim_namespace_json(args)
        json_data = json.dumps(change_output(remove_output(args)))

        response_json, status_code = VolumeConfiguration.add_volume_config(
            json_data)
        confirm_output(response_json, status_code, trim_json_data)
    except Exception as e:
        logger.exception(e)
        sys.exit(-1)


def list_volume(args):
    try:
        json_data = trim_namespace_json(args)

        if (json_data.get("cloud_provider")):
            response_json, status_code = VolumeConfiguration.list_volume_config(
                str(json_data.get("cloud_provider")).upper())
            confirm_output(response_json, status_code, json_data)
        else:
            response_json, status_code = VolumeConfiguration.list_volume_config()
            confirm_output(response_json, status_code, json_data)
    except Exception as e:
        logger.exception(e)
        sys.exit(-1)


def describe_volume(args):
    try:
        json_data = trim_namespace_json(args)

        response_json, status_code = VolumeConfiguration.get_volume_config_by_id(
            json_data.get('volume_conf_id')[0])
        confirm_output(response_json, status_code, json_data)
    except Exception as e:
        logger.exception(e)
        sys.exit(-1)


def edit_volume(args):
    try:
        trim_json_data = trim_namespace_json(args)

        json_data = change_output(remove_output(args))

        del json_data['volume_conf_id']

        json_data = json.dumps(json_data)

        response_json, status_code = VolumeConfiguration.edit_volume_config(
            trim_json_data.get('volume_conf_id')[0], json_data)
        confirm_output(response_json, status_code, trim_json_data)
    except Exception as e:
        logger.exception(e)
        sys.exit(-1)


# Network Configuration
def create_network(args):
    try:
        trim_json_data = trim_namespace_json(args)
        json_data = json.dumps(change_output(trim_network_config_json(args)))

        response_json, status_code = NetworkConfiguration.add_network_config_by_cp_id(
            trim_json_data.get('cloud_provider_id')[0], json_data)
        confirm_output(response_json, status_code, trim_json_data)
    except Exception as e:
        logger.exception(e)
        sys.exit(-1)


def list_provider_network(args):
    try:
        json_data = trim_namespace_json(args)

        if json_data.get('cloud_provider') is None:
            response_json, status_code = NetworkConfiguration.get_network_config_by_cp_id()
        else:
            response_json, status_code = NetworkConfiguration.get_network_config_by_cp_id(
                json_data.get('cloud_provider'))
        confirm_output(response_json, status_code, json_data)
    except Exception as e:
        logger.exception(e)
        sys.exit(-1)


def describe_provider_network(args):
    try:
        json_data = trim_namespace_json(args)

        response_json, status_code = NetworkConfiguration.get_network_config_by_cp_id_and_id(
            json_data.get('network_conf_id')[0])
        confirm_output(response_json, status_code, json_data)
    except Exception as e:
        logger.exception(e)
        sys.exit(-1)


def edit_provider_network(args):
    try:
        trim_json_data = trim_namespace_json(args)
        json_data = change_output(remove_output(args))

        del json_data['network_conf_id']

        json_data = json.dumps(json_data)

        response_json, status_code = NetworkConfiguration.modify_network_config_by_cp_id_and_id(
            trim_json_data.get('network_conf_id')[0], json_data)
        confirm_output(response_json, status_code, trim_json_data)
    except Exception as e:
        logger.exception(e)
        sys.exit(-1)


# Boot Disk Image Configuration
def create_boot_disk_image_config(args):
    try:
        trim_json_data = trim_namespace_json(args)
        json_data = change_output(remove_output(args))

        response_json, status_code = BootDiskImageConfiguration.add_boot_disk_image_config(
            json.dumps(json_data))
        confirm_output(response_json, status_code, trim_json_data)
    except Exception as e:
        logger.exception(e)
        sys.exit(-1)


def list_boot_disk_image_config(args):
    try:
        json_data = trim_namespace_json(args)

        if json_data.get('cloud_provider') is None:
            response_json, status_code = BootDiskImageConfiguration.list_boot_disk_image_config()
        else:
            response_json, status_code = BootDiskImageConfiguration.list_boot_disk_image_config(
                json_data.get('cloud_provider'))

        confirm_output(response_json, status_code, json_data)
    except Exception as e:
        logger.exception(e)
        sys.exit(-1)


def describe_boot_disk_image_config(args):
    try:
        json_data = trim_namespace_json(args)

        response_json, status_code = BootDiskImageConfiguration.get_boot_disk_image_config_by_id(
            json_data.get('boot_disk_image_id')[0])
        confirm_output(response_json, status_code, json_data)
    except Exception as e:
        logger.exception(e)
        sys.exit(-1)


# Machine Configuration
def create_machine(args):
    try:
        trim_json_data = trim_namespace_json(args)

        json_data = change_output(remove_output(args))

        if hasattr(args, 'bootstrap_shell_script_file_path') and trim_json_data.get('bootstrap_shell_script_file_path')[0] != None:
            bootstrapShellScript = checkUnixFileFormat(checkFilePathExists(
                trim_json_data.get('bootstrap_shell_script_file_path')[0], 'bootstrap_shell_script_file_path'))

            json_data["bootstrap_shell_script"] = appendSheBang(readFileContent(
                bootstrapShellScript))

            del json_data["bootstrap_shell_script_file_path"]

            json_data = json.dumps(json_data)

            response_json, status_code = MachineConfiguration.add_machine_config(
                json_data)

            confirm_output(response_json, status_code, trim_json_data)
        else:
            json_data = json.dumps(json_data)

            response_json, status_code = MachineConfiguration.add_machine_config(
                json_data)
            confirm_output(response_json, status_code, trim_json_data)
    except Exception as e:
        logger.exception(e)
        sys.exit(-1)


def describe_machine(args):
    try:
        json_data = trim_namespace_json(args)

        response_json, status_code = MachineConfiguration.get_machine_config_by_id(
            json_data.get('machine_conf_id')[0])
        confirm_output(response_json, status_code, json_data)
    except Exception as e:
        logger.exception(e)
        sys.exit(-1)


def list_machine(args):
    try:
        json_data = trim_namespace_json(args)

        if (json_data.get("cloud_provider")):
            response_json, status_code = MachineConfiguration.list_machine_config(
                str(json_data.get("cloud_provider")).upper())
            confirm_output(response_json, status_code, json_data)
        else:
            response_json, status_code = MachineConfiguration.list_machine_config()
            confirm_output(response_json, status_code, json_data)
    except Exception as e:
        logger.exception(e)
        sys.exit(-1)


def edit_machine(args):
    try:
        trim_json_data = trim_namespace_json(args)
        json_data = change_output(remove_output(args))

        del json_data['machine_conf_id']

        if hasattr(args, 'bootstrap_shell_script_file_path') and trim_json_data.get('bootstrap_shell_script_file_path') != None:
            bootstrapShellScript = checkUnixFileFormat(checkFilePathExists(
                trim_json_data.get('bootstrap_shell_script_file_path'), 'bootstrap_shell_script_file_path'))

            json_data["bootstrap_shell_script"] = appendSheBang(readFileContent(
                bootstrapShellScript))

            del json_data["bootstrap_shell_script_file_path"]

        json_data = json.dumps(json_data)

        response_json, status_code = MachineConfiguration.edit_machine_config(
            trim_json_data.get('machine_conf_id')[0], json_data)
        confirm_output(response_json, status_code, trim_json_data)
    except Exception as e:
        logger.exception(e)
        sys.exit(-1)


# Credentials Configuration
def create_credential(args):
    try:
        trim_json_data = trim_namespace_json(args)
        json_data = json.dumps(change_output(remove_output(args)))

        response_json, status_code = CredentialsConfig.add_credentials_config(
            json_data)
        confirm_output(response_json, status_code, trim_json_data)
    except Exception as e:
        logger.exception(e)
        sys.exit(-1)


def list_credential(args):
    try:
        json_data = trim_namespace_json(args)

        if (json_data.get("cloud_provider")):
            response_json, status_code = CredentialsConfig.list_credentials_config(
                str(json_data.get("cloud_provider")).upper())
            confirm_output(response_json, status_code, json_data)
        else:
            response_json, status_code = CredentialsConfig.list_credentials_config()
            confirm_output(response_json, status_code, json_data)
    except Exception as e:
        logger.exception(e)
        sys.exit(-1)


def describe_credential(args):
    try:
        json_data = trim_namespace_json(args)

        response_json, status_code = CredentialsConfig.get_credentials_config_by_id(
            json_data.get('credentials_conf_id')[0])
        confirm_output(response_json, status_code, json_data)
    except Exception as e:
        logger.exception(e)
        sys.exit(-1)


def edit_credential(args):
    try:
        trim_json_data = trim_namespace_json(args)
        json_data = change_output(remove_output(args))

        del json_data["credentials_conf_id"]

        json_data = json.dumps(json_data)

        response_json, status_code = CredentialsConfig.edit_credentials_config(
            trim_json_data.get('credentials_conf_id')[0], json_data)
        confirm_output(response_json, status_code, trim_json_data)
    except Exception as e:
        logger.exception(e)
        sys.exit(-1)


def delete_credential(args):
    try:
        trim_json_data = trim_namespace_json(args)

        response_json, status_code = CredentialsConfig.delete_credentials_config_by_id(
            trim_json_data.get('credentials_conf_id')[0])
        confirm_output(response_json, status_code, trim_json_data)
    except Exception as e:
        logger.exception(e)
        sys.exit(-1)


# Object Storage Manager Configuration
def create_object_storage_manager(args):
    try:
        trim_json_data = trim_namespace_json(args)
        json_data = json.dumps(change_output(remove_output(args)))

        response_json, status_code = ObjectStorageManager.add_object_storage_manager(
            json_data)
        confirm_output(response_json, status_code, trim_json_data)
    except Exception as e:
        logger.exception(e)
        sys.exit(-1)


def list_object_storage_manager(args):
    try:
        json_data = trim_namespace_json(args)

        if (json_data.get("cloud_provider")):
            response_json, status_code = ObjectStorageManager.list_object_storage_manager(
                str(json_data.get("cloud_provider")).upper())
            confirm_output(response_json, status_code, json_data)
        else:
            response_json, status_code = ObjectStorageManager.list_object_storage_manager()
            confirm_output(response_json, status_code, json_data)
    except Exception as e:
        logger.exception(e)
        sys.exit(-1)


def get_object_storage_manager(args):
    try:
        json_data = trim_namespace_json(args)

        response_json, status_code = ObjectStorageManager.get_object_storage_manager_by_object_storage_manager_id(
            json_data.get('object_storage_manager_id')[0])
        confirm_output(response_json, status_code, json_data)
    except Exception as e:
        logger.exception(e)
        sys.exit(-1)


def edit_object_storage_manager(args):
    try:
        trim_json_data = trim_namespace_json(args)
        json_data = change_output(remove_output(args))

        del json_data["object_storage_manager_id"]

        json_data = json.dumps(json_data)

        response_json, status_code = ObjectStorageManager.edit_object_storage_manager(
            trim_json_data.get('object_storage_manager_id')[0], json_data)
        confirm_output(response_json, status_code, trim_json_data)
    except Exception as e:
        logger.exception(e)
        sys.exit(-1)


def delete_object_storage_manager(args):
    try:
        trim_json_data = trim_namespace_json(args)
        response_json, status_code = ObjectStorageManager.delete_object_storage_manager(
            trim_json_data.get('object_storage_manager_id')[0])
        confirm_output(response_json, status_code, trim_json_data)
    except Exception as e:
        logger.exception(e)
        sys.exit(-1)


# Object Storage Manager Files Configuration
def create_object_storage_manager_files(args):
    try:
        trim_json_data = change_output(trim_namespace_json(args))

        json_data = change_output(remove_output(args))

        if (trim_json_data.get('local_file_path') != None and os.path.isfile(trim_json_data.get('local_file_path'))):

            response_json, status_code = ObjectStorageManagerFiles.add_object_storage_manager_files(
                trim_json_data.get('object_storage_manager_id'),
                trim_json_data.get('local_file_path'),
                trim_json_data.get('preserve_path'),
                trim_json_data.get('overwrite')
            )
            confirm_output(response_json, status_code, trim_json_data)

        elif (trim_json_data.get('local_file_path') == None):
            logger.error("Please provide a local file path\n")
            sys.exit(-1)

        else:
            file_error = {
                "error": f"The file cannot be found at {trim_json_data.get('local_file_path')[0]}"}
            logger.error(json.dumps(file_error, indent=2))
            sys.exit(-1)
    except Exception as e:
        logger.exception(e)
        sys.exit(-1)


def get_object_storage_manager_files(args):
    try:
        json_data = trim_namespace_json(args)

        if (json_data.get('object_storage_manager_id') and json_data.get('file_id') == None):
            response_json, status_code = ObjectStorageManagerFiles.get_object_storage_manager_files_by_object_storage_manager_id(
                json_data.get('object_storage_manager_id')[0])
            confirm_output(response_json, status_code, json_data)

        elif (json_data.get('object_storage_manager_id') and json_data.get('file_id')):
            response_json, status_code = ObjectStorageManagerFiles.get_object_storage_manager_files_by_object_storage_manager_id(
                json_data.get('object_storage_manager_id')[0], json_data.get('file_id')[0])
            confirm_output(response_json, status_code, json_data)
    except Exception as e:
        logger.exception(e)
        sys.exit(-1)


def delete_object_storage_manager_files(args):
    try:
        trim_json_data = change_output(trim_namespace_json(args))

        response_json, status_code = ObjectStorageManagerFiles.delete_object_storage_manager_file(
            trim_json_data.get('object_storage_manager_id'),
            trim_json_data.get('file_id')
        )
        confirm_output(response_json, status_code, trim_json_data)
    except Exception as e:
        logger.exception(e)
        sys.exit(-1)


# Hive Metastore Configuration
def create_hive_metastore_config(args):
    try:
        trim_json_data = trim_namespace_json(args)
        json_data = createOrUpdateHiveMetastoreConfig(
            change_output(remove_output(args)))

        response_json, status_code = HiveMetastoreConfiguration.add_hive_metastore_configuration(
            json_data)

        confirm_output(response_json, status_code, trim_json_data)
    except Exception as e:
        logger.exception(e)
        sys.exit(-1)


def list_hive_metastore_config(args):
    try:
        json_data = trim_namespace_json(args)

        response_json, status_code = HiveMetastoreConfiguration.list_hive_metastore_config()
        confirm_output(response_json, status_code, json_data)
    except Exception as e:
        logger.exception(e)
        sys.exit(-1)


def describe_hive_metastore_config(args):
    try:
        json_data = trim_namespace_json(args)

        response_json, status_code = HiveMetastoreConfiguration.get_hive_metastore_config_by_id(
            json_data.get('hive_metastore_conf_id')[0])
        confirm_output(response_json, status_code, json_data)
    except Exception as e:
        logger.exception(e)
        sys.exit(-1)


def edit_hive_metastore_config(args):
    try:
        trim_json_data = trim_namespace_json(args)

        json_data = createOrUpdateHiveMetastoreConfig(
            change_output(remove_output(args)))

        response_json, status_code = HiveMetastoreConfiguration.edit_hive_metastore_config(
            trim_json_data.get('hive_metastore_conf_id')[0], json_data)

        confirm_output(response_json, status_code, trim_json_data)
    except Exception as e:
        logger.exception(e)
        sys.exit(-1)


def delete_hive_metastore_config(args):
    try:
        trim_json_data = trim_namespace_json(args)

        response_json, status_code = HiveMetastoreConfiguration.delete_hive_metastore_config_by_id(
            trim_json_data.get('hive_metastore_conf_id')[0])

        confirm_output(response_json, status_code, trim_json_data)
    except Exception as e:
        logger.exception(e)
        sys.exit(-1)
