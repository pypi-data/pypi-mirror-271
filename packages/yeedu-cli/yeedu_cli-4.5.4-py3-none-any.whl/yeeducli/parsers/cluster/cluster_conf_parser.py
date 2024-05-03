from yeeducli.constants import CLUSTER_TYPE_LIST, CLOUD_PROVIDERS_LIST
from argparse import SUPPRESS, ArgumentDefaultsHelpFormatter


class ClusterConfigurationParser:

    def cluster_configuration_parser(subparser):

        create_cluster_conf = subparser.add_parser(
            'create-conf',
            help='To create the Cluster Configuration.',
            formatter_class=ArgumentDefaultsHelpFormatter)
        create_cluster_conf.add_argument(
            "--name",
            type=str,
            nargs=1,
            default=SUPPRESS,
            required=True,
            help="Provide name to create-conf."
        )
        create_cluster_conf.add_argument(
            "--description",
            type=str,
            nargs=1,
            default=SUPPRESS,
            required=True,
            help="Provide description to create-conf."
        )
        create_cluster_conf.add_argument(
            "--cloud_project_id",
            type=str,
            nargs=1,
            default=SUPPRESS,
            required=True,
            help="Provide cloud_project_id to create-conf."
        )
        create_cluster_conf.add_argument(
            "--object_storage_manager_id",
            type=int,
            nargs=1,
            default=SUPPRESS,
            required=True,
            help="Provide object_storage_manager_id to create-conf."
        )
        create_cluster_conf.add_argument(
            "--credentials_conf_id",
            type=int,
            nargs=1,
            default=SUPPRESS,
            required=True,
            help="Provide credentials_conf_id to create-conf."
        )
        create_cluster_conf.add_argument(
            "--machine_conf_id",
            type=int,
            nargs=1,
            default=SUPPRESS,
            required=True,
            help="Provide machine_conf_id to create-conf."
        )
        create_cluster_conf.add_argument(
            "--spark_config_id",
            type=int,
            nargs='?',
            default=SUPPRESS,
            help="Provide spark_config_id to create-conf."
        )
        create_cluster_conf.add_argument(
            "--hive_metastore_conf_id",
            type=int,
            nargs='?',
            default=SUPPRESS,
            help="Provide hive_metastore_conf_id to create-conf."
        )
        create_cluster_conf.add_argument(
            "--cloud_provider_id",
            type=int,
            nargs=1,
            default=SUPPRESS,
            required=True,
            help="Provide cloud_provider_id to create-conf."
        )
        create_cluster_conf.add_argument(
            "--spark_infra_version_id",
            type=int,
            nargs=1,
            default=SUPPRESS,
            required=True,
            help="Provide spark_infra_version_id to create-conf."
        )
        create_cluster_conf.add_argument(
            "--max_parallel_spark_job_execution_per_instance",
            type=int,
            nargs='?',
            default=5,
            help="Provide max_parallel_spark_job_execution_per_instance to create-conf."
        )
        create_cluster_conf.add_argument(
            "--standalone_workers_number",
            type=int,
            nargs='?',
            default=SUPPRESS,
            help="Provide standalone_workers_number to create-conf."
        )
        create_cluster_conf.add_argument(
            "--cluster_type",
            type=str,
            nargs=1,
            default=SUPPRESS,
            required=True,
            choices=CLUSTER_TYPE_LIST,
            metavar='YEEDU, STANDALONE, CLUSTER',
            help="Provide cluster_type to create-conf."
        )
        create_cluster_conf.add_argument(
            "--min_instances",
            type=int,
            nargs=1,
            default=SUPPRESS,
            required=True,
            help="Provide min_instances to create-conf."
        )
        create_cluster_conf.add_argument(
            "--max_instances",
            type=int,
            nargs=1,
            default=SUPPRESS,
            required=True,
            help="Provide max_instances to create-conf."
        )
        create_cluster_conf.add_argument(
            "--is_cuda",
            type=str,
            nargs=1,
            default=SUPPRESS,
            metavar='true,false',
            required=True,
            help="Provide is_cuda to create-conf."
        )
        create_cluster_conf.add_argument(
            "--json-output",
            type=str,
            nargs='?',
            choices=['pretty', 'default'],
            default='pretty',
            help="Provide the format of JSON output."
        )
        create_cluster_conf.add_argument(
            "--yaml-output",
            type=str,
            nargs='?',
            choices=['true', 'false'],
            default='false',
            help="Provide true to get output in YAML format."
        )

        list_cluster_conf = subparser.add_parser(
            'list-confs',
            help='To list all the available Cluster Configurations.',
            formatter_class=ArgumentDefaultsHelpFormatter)
        list_cluster_conf.add_argument(
            "--cloud_provider",
            type=str,
            nargs='?',
            default=SUPPRESS,
            choices=CLOUD_PROVIDERS_LIST,
            help="Cloud Provider that will be used for filtering list."
        )
        list_cluster_conf.add_argument(
            "--page_number",
            # type=check_minimum,
            type=int,
            nargs=1,
            default=1,
            help="To list Engine Cluser Configuration for a specific page_number."
        )
        list_cluster_conf.add_argument(
            "--limit",
            # type=check_range(1, 1000),
            type=int,
            nargs=1,
            default=100,
            help="Provide limit to list number of Engine Cluser Configuration."
        )
        list_cluster_conf.add_argument(
            "--json-output",
            type=str,
            nargs='?',
            choices=['pretty', 'default'],
            default='pretty',
            help="Provide the format of JSON output."
        )
        list_cluster_conf.add_argument(
            "--yaml-output",
            type=str,
            nargs='?',
            choices=['true', 'false'],
            default='false',
            help="Provide true to get output in YAML format."
        )

        get_cluster_conf = subparser.add_parser(
            'get-conf',
            help='To get the information about a specific Cluster Configuration.',
            formatter_class=ArgumentDefaultsHelpFormatter)
        get_cluster_conf.add_argument(
            "--cluster_conf_id",
            type=int,
            nargs=1,
            default=SUPPRESS,
            help="Provide Cluster Conf Id to get information about a specific Cluster Configuration."
        )
        get_cluster_conf.add_argument(
            "--cluster_conf_name",
            type=str,
            nargs=1,
            default=SUPPRESS,
            help="Provide Engine Cluster Config Name to get information about a specific Cluster Configuration."
        )
        get_cluster_conf.add_argument(
            "--json-output",
            type=str,
            nargs='?',
            choices=['pretty', 'default'],
            default='pretty',
            help="Provide the format of JSON output."
        )
        get_cluster_conf.add_argument(
            "--yaml-output",
            type=str,
            nargs='?',
            choices=['true', 'false'],
            default='false',
            help="Provide true to get output in YAML format."
        )

        edit_cluster_conf = subparser.add_parser(
            'edit-conf',
            help='To edit a specific Cluster Configuration.',
            formatter_class=ArgumentDefaultsHelpFormatter)
        edit_cluster_conf.add_argument(
            "--cluster_conf_id",
            type=int,
            nargs=1,
            default=SUPPRESS,
            help="Provide a specific Cluster Conf Id to edit-conf."
        )
        edit_cluster_conf.add_argument(
            "--cluster_conf_name",
            type=str,
            nargs=1,
            default=SUPPRESS,
            help="Provide a specific Engine Cluster Config Name to edit-conf."
        )
        edit_cluster_conf.add_argument(
            "--name",
            type=str,
            nargs='?',
            default=SUPPRESS,
            help="Provide name to edit-conf."
        )
        edit_cluster_conf.add_argument(
            "--description",
            type=str,
            nargs='?',
            default=SUPPRESS,
            help="Provide description to edit-conf."
        )
        edit_cluster_conf.add_argument(
            "--cloud_project_id",
            type=str,
            nargs='?',
            default=SUPPRESS,
            help="Provide cloud_project_id to edit-conf."
        )
        edit_cluster_conf.add_argument(
            "--max_parallel_spark_job_execution_per_instance",
            type=int,
            nargs='?',
            default=SUPPRESS,
            help="Provide max_parallel_spark_job_execution_per_instance to edit-conf."
        )
        edit_cluster_conf.add_argument(
            "--standalone_workers_number",
            type=int,
            nargs='?',
            default=SUPPRESS,
            help="Provide standalone_workers_number to edit-conf."
        )
        edit_cluster_conf.add_argument(
            "--cluster_type",
            type=str,
            nargs=1,
            default=SUPPRESS,
            choices=CLUSTER_TYPE_LIST,
            metavar='YEEDU, STANDALONE, CLUSTER',
            help="Provide cluster_type to edit-conf."
        )
        edit_cluster_conf.add_argument(
            "--min_instances",
            type=int,
            nargs='?',
            default=SUPPRESS,
            help="Provide min_instances to edit-conf."
        )
        edit_cluster_conf.add_argument(
            "--max_instances",
            type=int,
            nargs='?',
            default=SUPPRESS,
            help="Provide max_instances to edit-conf."
        )
        edit_cluster_conf.add_argument(
            "--is_cuda",
            type=str,
            nargs='?',
            default=SUPPRESS,
            metavar='true,false',
            help="Provide is_cuda to edit-conf."
        )
        edit_cluster_conf.add_argument(
            "--json-output",
            type=str,
            nargs='?',
            choices=['pretty', 'default'],
            default='pretty',
            help="Provide the format of JSON output."
        )
        edit_cluster_conf.add_argument(
            "--yaml-output",
            type=str,
            nargs='?',
            choices=['true', 'false'],
            default='false',
            help="Provide true to get output in YAML format."
        )
