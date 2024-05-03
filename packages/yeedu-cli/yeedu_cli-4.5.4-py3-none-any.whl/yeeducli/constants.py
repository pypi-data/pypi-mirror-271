from os.path import join
from dotenv import load_dotenv
import logging
import os
import sys

load_dotenv()

HOME = os.path.expanduser('~')

YEEDU_HIDDEN_DIR = join(HOME, '.yeedu')

DEFAULT_CLI_LOG_PATH = join(join(YEEDU_HIDDEN_DIR, 'cli'), 'logs')

if os.getenv('YEEDU_RESTAPI_TOKEN_FILE_PATH') is not None:

    if os.path.isdir(os.getenv('YEEDU_RESTAPI_TOKEN_FILE_PATH')):
        logging.error(
            f"Provided environment variable :'YEEDU_RESTAPI_TOKEN_FILE_PATH: {os.getenv('YEEDU_RESTAPI_TOKEN_FILE_PATH')}' doenot contain filename or directory not found.")
        sys.exit(-1)
    else:
        CONFIG_FILE_PATH = os.getenv('YEEDU_RESTAPI_TOKEN_FILE_PATH')
else:
    CONFIG_FILE_PATH = join(YEEDU_HIDDEN_DIR, 'yeedu_cli.config')


def check_environment_variable_int(variable_name, default_value):
    value = os.getenv(variable_name)
    if value is None:
        return default_value

    try:
        int_value = int(value)
    except ValueError:
        raise ValueError(
            f"Environment variable: {variable_name} must include only integers but found: {value}")

    return int_value


try:
    YEEDU_CLI_MAX_LOG_FILES = check_environment_variable_int(
        "YEEDU_CLI_MAX_LOG_FILES", 5)
    YEEDU_CLI_MAX_LOG_FILE_SIZE = check_environment_variable_int(
        "YEEDU_CLI_MAX_LOG_FILE_SIZE", 30)

except ValueError as e:
    logging.error(f"Error: {e}")
    sys.exit(-1)

CREDENTIALS_FILE_PATH = join(YEEDU_HIDDEN_DIR, 'yeedu_credentials.config')

# CLOUD PROVIDERS
CLOUD_PROVIDERS_LIST = ['GCP', 'AWS', 'AZURE']

# CLUSTER TYPEs
CLUSTER_TYPE_LIST = ['YEEDU', 'STANDALONE', 'CLUSTER']

# SPARK DEPLOYMENT MODEs
SPARK_DEPLOYMENT_MODE_LIST = ['client', 'cluster']

# SPARK JOB STATUS
SPARK_JOB_STATUS = ['submitted', 'running', 'done',
                    'error', 'terminated', 'killing', 'killed']

# RESOURCE SUBCOMMANDS LIST
RESOURCE_LIST = ['list-providers', 'list-disk-machine-types', 'list-credential-types', 'list-engine-cluster-instance-status', 'get-provider', 'list-provider-availability-zones', 'get-provider-availability-zone', 'list-provider-machine-types', 'get-provider-machine-type', 'list-spark-compute-types', 'list-spark-infra-versions', 'list-spark-job-status', 'list-workflow-execution-states', 'list-workflow-types', 'create-volume-conf', 'get-volume-conf', 'list-volume-confs', 'edit-volume-conf', 'create-network-conf', 'list-network-confs', 'get-network-conf', 'edit-network-conf', 'create-boot-disk-image-conf', 'list-boot-disk-image-confs', 'get-boot-disk-image-conf', 'create-machine-conf', 'get-machine-conf', 'list-machine-confs', 'edit-machine-conf', 'create-object-storage-manager', 'get-object-storage-manager', 'list-object-storage-managers',
                 'edit-object-storage-manager', 'delete-object-storage-manager', 'create-object-storage-manager-file', 'get-object-storage-manager-file', 'list-object-storage-manager-files', 'delete-object-storage-manager-file', 'create-hive-metastore-conf', 'list-hive-metastore-confs', 'get-hive-metastore-conf', 'edit-hive-metastore-conf', 'delete-hive-metastore-conf', 'create-credential-conf', 'list-credential-confs', 'get-credential-conf', 'edit-credential-conf', 'delete-credential-conf']

# CLUSTER SUBCOMMANDS LIST
CLUSTER_LIST = ['create-conf', 'list-confs', 'get-conf', 'edit-conf',
                'create', 'list', 'get', 'edit', 'destroy', 'uptime', 'start', 'stop', 'get-stats', 'logs']

# USI SUBCOMMANDS LIST
JOB_LIST = ['create-conf', 'get-conf', 'list-confs', 'edit-conf', 'delete-conf',
            'start', 'get', 'list', 'kill', 'logs', 'get-workflow-job-instance']

# IAM SUBCOMMANDS LIST
IAM_LIST = ['list-tenants', 'associate-tenant', 'get-user-info', 'get-user-roles', 'sync-user', 'sync-group', 'list-user-groups', 'list-users',
            'list-group-users', 'list-groups', 'list-resources', 'get-resource', 'list-permissions', 'get-permission', 'list-roles', 'get-role', 'list-rules', 'get-rule', 'search-user', 'search-group']

# ADMIN SUBCOMMANDS LIST
ADMIN_LIST = ['list-users', 'get-user', 'get-user-roles', 'list-users-roles', 'get-role-users', 'list-groups', 'get-group',
              'get-group-roles', 'list-groups-roles', 'get-role-groups', 'create-user-role', 'delete-user-role', 'create-group-role', 'delete-group-role']

# PLATFORM ADMIN SUBCOMMANDS LIST
PLATFORM_ADMIN_LIST = ['create-tenant', 'list-tenants', 'get-tenant', 'edit-tenant', 'delete-tenant', 'list-tenant-users', 'list-tenant-groups', 'get-tenant-user', 'get-tenant-group', 'get-user-roles',
                       'get-group-roles', 'list-user-tenants', 'get-role-users', 'list-users-roles', 'list-groups-roles', 'get-role-groups', 'create-user-role', 'delete-user-role', 'create-group-role', 'delete-group-role', 'search-tenant']

# COMMON PLATFORM AND ADMIN SUBCOMMANDS LIST
COMMON_PLATFORM_AND_ADMIN_LIST = ['list-users', 'get-user', 'get-user-roles', 'get-role-users', 'list-groups', 'get-group', 'get-group-roles', 'get-role-groups', 'create-user-role', 'delete-user-role',
                                  'create-group-role', 'delete-group-role' 'list-tenant-users', 'list-tenant-groups', 'get-tenant-user', 'get-tenant-group', 'get-user-roles', 'get-group-roles', 'get-role-users', 'get-role-groups']


# Columns list having data type as varchar array
VARCHAR_ARRAY_COLUMN_LIST = ['files', 'properties_file',
                             'packages', 'repositories', 'jars', 'archives']

VARCHAR_ARRAY_COLUMN_FULL_LIST = ['labels', 'conf', 'network_tags', 'files',
                                  'properties_file', 'packages', 'repositories', 'jars', 'archives']

# Columns list having data type as json
# JSON_ARGUMENTS_LIST = []

# JSON Samples used in validateJSON
VALID_JSON = """'{"a":"b","c":1}'"""

INVALID_JSON = '''{"a":"b","c":1}'''

# TAG Samples used in network_tags_validator
VALID_NETWORK_TAG = 'key1,value1,key2,value2'

INVALID_NETWORK_TAG = 'key1,value1,key2'

CLOUD_PROVIDER_AVAILABILITY_ZONE_ORDER = [
    'availability_zone_id', 'cloud_provider', 'name', 'region', 'description', 'from_date', 'to_date']

CLOUD_PROVIDER_MACHINE_TYPE_ORDER = [
    'machine_type_id', 'cloud_provider', 'name', 'vcpus', 'memory', 'has_cuda', 'gpu_model', 'gpus', 'gpu_memory',  'from_date', 'to_date']

CLOUD_PROVIDER_DISK_MACHINE_TYPE_ORDER = ['disk_type_id', 'cloud_provider',
                                          'name', 'has_fixed_size', 'min_size', 'max_size', 'from_date', 'to_date']

VOLUME_CONFIG_ORDER = ['volume_conf_id', 'name', 'availability_zone', 'encrypted', 'size', 'disk_type', 'machine_volume_num',
                       'machine_volume_strip_num', 'tenant_id', 'created_by', 'modified_by', 'last_update_date', 'from_date', 'to_date']

NETWORK_CONFIG_ORDER = ['network_conf_id', 'network_project_id', 'network_name', 'subnet', 'availability_zone',
                        'cloud_provider', 'tenant_id', 'created_by', 'modified_by', 'last_update_date',  'from_date', 'to_date']

BOOT_DISK_IMAGE_CONFIG_ORDER = ['boot_disk_image_id', 'boot_disk_image', 'cloud_provider',
                                'tenant_id', 'created_by', 'modified_by', 'last_update_date', 'from_date', 'to_date']

MACHINE_CONFIG_ORDER = ['machine_conf_id', 'network_tags', 'labels', 'service_account_instance_profile', 'boot_disk_image_config', 'machine_type', 'is_spot_instance', 'enable_public_ip',
                        'block_project_ssh_keys', 'bootstrap_shell_script', 'machine_network', 'machine_volume_config', 'tenant_id', 'created_by', 'modified_by', 'last_update_date', 'from_date', 'to_date']

CREDENTIALS_CONFIG_ORDER = ['credentials_conf_id', 'credential_type', 'name',
                            'tenant_id', 'created_by', 'modified_by', 'last_update_date', 'from_date', 'to_date']

OBJECT_STORAGE_MANAGER_ORDER = ['object_storage_manager_id', 'name', 'credentials_config',
                                'object_storage_bucket_name', 'tenant_id', 'created_by', 'modified_by', 'last_update_date', 'from_date', 'to_date']

OBJECT_STORAGE_MANAGER_FILES_ORDER = ['object_storage_manager_file_id', 'object_storage_manager', 'file_name', 'full_file_path',
                                      'file_size_bytes', 'file_type', 'local_file_path', 'tenant_id', 'created_by', 'modified_by', 'last_update_date', 'from_date', 'to_date']

ENGINE_CLUSTER_CONFIG_ORDER = ['cluster_conf_id', 'name', 'description', 'cloud_project_id', 'object_storage_manager', 'credentials_conf_id', 'machine_config', 'spark_config', 'hive_metastore', 'cloud_provider',
                               'spark_infra_version', 'engine_cluster_spark_config', 'cluster_type', 'min_instances', 'max_instances', 'is_cuda', 'tenant_id', 'created_by', 'modified_by', 'last_update_date',  'from_date', 'to_date']

SPARK_JOB_CONFIG_ORDER = ['job_conf_id', 'name', 'cluster_id', 'deploy_mode', 'max_concurrency', 'class_name', 'command', 'arguments', 'rawScalaCode', 'files', 'properties_file', 'conf', 'packages', 'repositories', 'jars', 'archives', 'driver_memory', 'driver_java_options',
                          'driver_library_path', 'driver_class_path', 'executor_memory', 'driver_cores', 'total_executor_cores', 'executor_cores', 'num_executors', 'principal', 'keytab', 'queue', 'tenant_id', 'created_by', 'modified_by', 'last_update_date', 'from_date', 'to_date']

USER_ROLES_ORDER = ['user_roles_id', 'tenant',
                    'user', 'role', 'from_date', 'to_date']

ADMIN_GROUP_ORDER = ['group_id', 'group_name', 'from_date', 'to_date']

USER_GROUP_ORDER = ['group', 'user', 'from_date', 'to_date']

GROUP_ROLE_ORDER = ['group_roles_id', 'tenant',
                    'group', 'role', 'from_date', 'to_date']

TENANT_ORDER = ['tenant_id', 'name', 'description', 'created_by',
                'modified_by', 'last_update_date', 'from_date', 'to_date']

LOOKUP_AUTH_RULES_ORDER = ['rule_id', 'permission_type',
                           'resource', 'role', 'from_date', 'to_date']

LOOKUP_CREDENTIAL_TYPES_ORDER = [
    'credential_type_id', 'name', 'cloud_provider', 'from_date', 'to_date']
