from yeeducli.constants import CLOUD_PROVIDERS_LIST
from argparse import SUPPRESS, ArgumentDefaultsHelpFormatter


class VolumeConfigurationParser:

    def volume_configuration_parser(subparser):
        create_volume_conf = subparser.add_parser(
            'create-volume-conf',
            help='To create the Volume Configuration.',
            formatter_class=ArgumentDefaultsHelpFormatter)
        create_volume_conf.add_argument(
            "--name",
            type=str,
            nargs='?',
            default=SUPPRESS,
            required=True,
            help="Provide name to create-volume-conf."
        )
        create_volume_conf.add_argument(
            "--availability_zone_id",
            type=int,
            nargs=1,
            default=SUPPRESS,
            required=True,
            help="Provide availability_zone_id to create-volume-conf."
        )
        create_volume_conf.add_argument(
            "--encrypted",
            type=str,
            nargs=1,
            default=SUPPRESS,
            metavar='true,false',
            required=True,
            help="Provide encrypted to create-volume-conf."
        )
        create_volume_conf.add_argument(
            "--size",
            type=int,
            nargs='?',
            default=SUPPRESS,
            help="Provide size to create-volume-conf."
        )
        create_volume_conf.add_argument(
            "--disk_type_id",
            type=int,
            nargs=1,
            default=SUPPRESS,
            required=True,
            help="Provide disk_type to create-volume-conf."
        )
        create_volume_conf.add_argument(
            "--machine_volume_num",
            type=int,
            nargs=1,
            default=SUPPRESS,
            required=True,
            help="Provide machine_volume_num to create-volume-conf."
        )
        create_volume_conf.add_argument(
            "--machine_volume_strip_num",
            type=int,
            nargs=1,
            default=SUPPRESS,
            required=True,
            help="Provide machine_volume_strip_num to create-volume-conf."
        )
        create_volume_conf.add_argument(
            "--json-output",
            type=str,
            nargs='?',
            choices=['pretty', 'default'],
            default='pretty',
            help="Provide the format of JSON output."
        )
        create_volume_conf.add_argument(
            "--yaml-output",
            type=str,
            nargs='?',
            choices=['true', 'false'],
            default='false',
            help="Provide true to get output in YAML format."
        )

        describe_volume_conf = subparser.add_parser(
            'get-volume-conf',
            help='To get information about a specific Volume Configuration.',
            formatter_class=ArgumentDefaultsHelpFormatter)
        describe_volume_conf.add_argument(
            "--volume_conf_id",
            type=int,
            nargs=1,
            default=SUPPRESS,
            required=True,
            help="Provide volume_conf_id to get information about a specific Volume Configuration."
        )
        describe_volume_conf.add_argument(
            "--json-output",
            type=str,
            nargs='?',
            choices=['pretty', 'default'],
            default='pretty',
            help="Provide the format of JSON output."
        )
        describe_volume_conf.add_argument(
            "--yaml-output",
            type=str,
            nargs='?',
            choices=['true', 'false'],
            default='false',
            help="Provide true to get output in YAML format."
        )

        list_volume_conf = subparser.add_parser(
            'list-volume-confs',
            help='To list all the available Volume Configurations.',
            formatter_class=ArgumentDefaultsHelpFormatter)
        list_volume_conf.add_argument(
            "--cloud_provider",
            type=str,
            nargs='?',
            choices=CLOUD_PROVIDERS_LIST,
            default=SUPPRESS,
            help="Cloud Provider that will be used for filtering list."
        )
        list_volume_conf.add_argument(
            "--json-output",
            type=str,
            nargs='?',
            choices=['pretty', 'default'],
            default='pretty',
            help="Provide the format of JSON output."
        )
        list_volume_conf.add_argument(
            "--yaml-output",
            type=str,
            nargs='?',
            choices=['true', 'false'],
            default='false',
            help="Provide true to get output in YAML format."
        )

        edit_volume_conf = subparser.add_parser(
            'edit-volume-conf',
            help='To edit a specific Volume Configuration.',
            formatter_class=ArgumentDefaultsHelpFormatter)
        edit_volume_conf.add_argument(
            "--volume_conf_id",
            type=int,
            nargs=1,
            default=SUPPRESS,
            required=True,
            help="Provide specific volume_conf_id to edit-volume-conf."
        )
        edit_volume_conf.add_argument(
            "--name",
            type=str,
            nargs='?',
            default=SUPPRESS,
            help="Provide name to edit-volume-conf."
        )
        edit_volume_conf.add_argument(
            "--encrypted",
            type=str,
            nargs='?',
            metavar='true,false',
            default=SUPPRESS,
            help="Provide encrypted to edit-volume-conf."
        )
        edit_volume_conf.add_argument(
            "--machine_volume_num",
            type=int,
            nargs=1,
            default=SUPPRESS,
            help="Provide machine_volume_num to edit-volume-conf."
        )
        edit_volume_conf.add_argument(
            "--machine_volume_strip_num",
            type=int,
            nargs=1,
            default=SUPPRESS,
            help="Provide machine_volume_strip_num to edit-volume-conf."
        )
        edit_volume_conf.add_argument(
            "--json-output",
            type=str,
            nargs='?',
            choices=['pretty', 'default'],
            default='pretty',
            help="Provide the format of JSON output."
        )
        edit_volume_conf.add_argument(
            "--yaml-output",
            type=str,
            nargs='?',
            choices=['true', 'false'],
            default='false',
            help="Provide true to get output in YAML format."
        )
