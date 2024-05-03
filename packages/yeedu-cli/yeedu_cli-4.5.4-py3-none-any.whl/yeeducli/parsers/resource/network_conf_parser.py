from argparse import SUPPRESS, ArgumentDefaultsHelpFormatter
from yeeducli.constants import CLOUD_PROVIDERS_LIST


class NetworkConfigurationParser:

    def network_configuration_parser(subparser):
        create_network_conf = subparser.add_parser(
            'create-network-conf',
            help='To create the Network Configuration.',
            formatter_class=ArgumentDefaultsHelpFormatter)
        create_network_conf.add_argument(
            "--network_project_id",
            type=str,
            nargs=1,
            default=SUPPRESS,
            required=True,
            help="Provide network_project_id to create-network-conf."
        )
        create_network_conf.add_argument(
            "--network_name",
            type=str,
            nargs=1,
            default=SUPPRESS,
            required=True,
            help="Provide network_name to create-network-conf."
        )
        create_network_conf.add_argument(
            "--subnet",
            type=str,
            nargs=1,
            default=SUPPRESS,
            required=True,
            help="Provide subnet to create-network-conf."
        )
        create_network_conf.add_argument(
            "--availability_zone_id",
            type=int,
            nargs=1,
            default=SUPPRESS,
            required=True,
            help="Provide availability_zone_id to create-network-conf."
        )
        create_network_conf.add_argument(
            "--cloud_provider_id",
            type=int,
            nargs=1,
            default=SUPPRESS,
            required=True,
            help="Provide cloud_provider_id to create-network-conf."
        )
        create_network_conf.add_argument(
            "--json-output",
            type=str,
            nargs='?',
            choices=['pretty', 'default'],
            default='pretty',
            help="Provide the format of JSON output."
        )
        create_network_conf.add_argument(
            "--yaml-output",
            type=str,
            nargs='?',
            choices=['true', 'false'],
            default='false',
            help="Provide true to get output in YAML format."
        )

        list_network_conf = subparser.add_parser(
            'list-network-confs',
            help='To get information about Network Configurations for a specific Cloud Provider.',
            formatter_class=ArgumentDefaultsHelpFormatter)
        list_network_conf.add_argument(
            "--cloud_provider",
            type=str,
            nargs='?',
            choices=CLOUD_PROVIDERS_LIST,
            default=SUPPRESS,
            help="Provide specific cloud_provider_id to get information about related Network Configurations."
        )
        list_network_conf.add_argument(
            "--json-output",
            type=str,
            nargs='?',
            choices=['pretty', 'default'],
            default='pretty',
            help="Provide the format of JSON output."
        )
        list_network_conf.add_argument(
            "--yaml-output",
            type=str,
            nargs='?',
            choices=['true', 'false'],
            default='false',
            help="Provide true to get output in YAML format."
        )

        describe_network_conf = subparser.add_parser(
            'get-network-conf',
            help='To get information about a specific Network Configuration for a specific Cloud Provider.',
            formatter_class=ArgumentDefaultsHelpFormatter)
        describe_network_conf.add_argument(
            "--network_conf_id",
            type=int,
            nargs=1,
            default=SUPPRESS,
            required=True,
            help="Provide id to get information about a specific network Configuration."
        )
        describe_network_conf.add_argument(
            "--json-output",
            type=str,
            nargs='?',
            choices=['pretty', 'default'],
            default='pretty',
            help="Provide the format of JSON output."
        )
        describe_network_conf.add_argument(
            "--yaml-output",
            type=str,
            nargs='?',
            choices=['true', 'false'],
            default='false',
            help="Provide true to get output in YAML format."
        )

        edit_network_conf = subparser.add_parser(
            'edit-network-conf',
            help='To edit a specific Network Configuration based on cloud provider Id and network Id.',
            formatter_class=ArgumentDefaultsHelpFormatter)
        edit_network_conf.add_argument(
            "--network_conf_id",
            type=int,
            nargs=1,
            default=SUPPRESS,
            required=True,
            help="Provide a specific Network Configuration id to edit-network-conf."
        )
        edit_network_conf.add_argument(
            "--network_name",
            type=str,
            nargs='?',
            default=SUPPRESS,
            help="Provide network_name to edit-network-conf."
        )
        edit_network_conf.add_argument(
            "--subnet",
            type=str,
            nargs='?',
            default=SUPPRESS,
            help="Provide subnet to edit-network-conf."
        )
        edit_network_conf.add_argument(
            "--json-output",
            type=str,
            nargs='?',
            choices=['pretty', 'default'],
            default='pretty',
            help="Provide the format of JSON output."
        )
        edit_network_conf.add_argument(
            "--yaml-output",
            type=str,
            nargs='?',
            choices=['true', 'false'],
            default='false',
            help="Provide true to get output in YAML format."
        )
