from yeeducli.parsers.resource.boot_disk_image_config_parser import BootDiskImageConfigurationParser
from yeeducli.parsers.resource.machine_conf_parser import MachineConfigurationParser
from yeeducli.parsers.resource.network_conf_parser import NetworkConfigurationParser
from yeeducli.parsers.resource.volume_conf_parser import VolumeConfigurationParser
from yeeducli.parsers.resource.credentials_conf_parser import CredentialsConfigurationParser
from yeeducli.parsers.resource.object_storage_manager_parser import ObjectStorageManagerParser
from yeeducli.parsers.resource.object_storage_manager_files_parser import ObjectStorageManagerFilesParser
from yeeducli.parsers.resource.hive_metastore_config_parser import HiveMetastoreConfigParser
from yeeducli.parsers.cluster.cluster_conf_parser import ClusterConfigurationParser
from yeeducli.parsers.cluster.cluster_inst_parser import ClusterInstanceParser
from yeeducli.parsers.resource.lookup_parser import LookupParser
from yeeducli.parsers.cluster.download_cluster_instance_log_parser import DownloadClusterInstanceLogParser
from yeeducli.parsers.job.spark_job_config_parser import SparkJobConfigurationParser
from yeeducli.parsers.job.spark_job_parser import SparkJobInstanceParser
from yeeducli.parsers.job.download_job_instance_log_parser import DownloadJobInstanceLogParser
from yeeducli.parsers.iam.user_parser import UserParser
from yeeducli.parsers.iam.shared_platform_and_admin_parser import SharedPlatformAndAdminParser
from yeeducli.parsers.iam.common_platform_and_admin_parser import CommonPlatformAndAdminParser
from yeeducli.parsers.iam.iam_lookup_parser import IamLookupParser
from yeeducli.parsers.iam.platform_admin_parser import PlatformAdminParser
from yeeducli.utility.logger_utils import Logger
import sys

logger = Logger.get_logger(__name__, True)


class ServiceParser:
    def create_service_parser(service, subparser):
        try:
            # RESOURCE
            if service == 'resource':

                LookupParser.lookup_parser(subparser)

                VolumeConfigurationParser.volume_configuration_parser(
                    subparser)

                NetworkConfigurationParser.network_configuration_parser(
                    subparser)

                BootDiskImageConfigurationParser.boot_disk_image_config_parser(
                    subparser)

                MachineConfigurationParser.machine_configuration_parser(
                    subparser)

                CredentialsConfigurationParser.credentials_config_parser(
                    subparser)

                ObjectStorageManagerParser.object_storage_manager_parser(
                    subparser)

                ObjectStorageManagerFilesParser.object_storage_manager_files_parser(
                    subparser)

                HiveMetastoreConfigParser.hive_metastore_config_parser(
                    subparser)

            # CLUSTER
            elif service == 'cluster':

                ClusterConfigurationParser.cluster_configuration_parser(
                    subparser)

                ClusterInstanceParser.cluster_instance_parser(subparser)

                DownloadClusterInstanceLogParser.download_cluster_instance_log_parser(
                    subparser)

            # USI
            elif service == 'job':

                SparkJobConfigurationParser.spark_job_configuration_parser(
                    subparser)

                SparkJobInstanceParser.spark_job_parser(subparser)

                DownloadJobInstanceLogParser.download_job_instance_log_parser(
                    subparser)

            # IAM
            elif service == 'iam':
                UserParser.user_parser(subparser)

                SharedPlatformAndAdminParser.shared_platform_and_admin_parser(
                    subparser)

                IamLookupParser.iam_lookup_parser(subparser)

            # ADMIN
            elif service == 'admin':

                CommonPlatformAndAdminParser.admin_parser(subparser)

            # PLATFORM ADMIN
            elif service == 'platform-admin':
                PlatformAdminParser.tenant_parser(subparser)

                PlatformAdminParser.platform_admin_parser(subparser)

                CommonPlatformAndAdminParser.platform_admin_parser(subparser)

        except Exception as e:
            logger.error(e)
            sys.exit(-1)
