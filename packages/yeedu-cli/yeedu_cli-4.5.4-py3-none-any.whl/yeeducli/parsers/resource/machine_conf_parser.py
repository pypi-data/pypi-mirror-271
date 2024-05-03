from yeeducli.constants import CLOUD_PROVIDERS_LIST
from argparse import SUPPRESS, ArgumentDefaultsHelpFormatter


class MachineConfigurationParser:

    def machine_configuration_parser(subparser):
        create_machine_conf = subparser.add_parser(
            'create-machine-conf',
            help='To create the Machine Configuration.',
            formatter_class=ArgumentDefaultsHelpFormatter)
        create_machine_conf.add_argument(
            "--network_tags",
            type=str,
            metavar=['value1,value2'],
            default=[],
            help="Provide network_tags to create-machine-conf."
        )
        create_machine_conf.add_argument(
            "--labels",
            type=str,
            action='append',
            default=SUPPRESS,
            nargs='+',
            help="Provide labels to create-machine-conf."
        )
        create_machine_conf.add_argument(
            "--service_account_instance_profile",
            type=str,
            nargs=1,
            default=SUPPRESS,
            required=True,
            help="Provide service_account_instance_profile to create-machine-conf."
        )
        create_machine_conf.add_argument(
            "--boot_disk_image_id",
            type=int,
            nargs=1,
            default=SUPPRESS,
            required=True,
            help="Provide boot_disk_image_id to create-machine-conf."
        )
        create_machine_conf.add_argument(
            "--machine_type_id",
            type=int,
            nargs=1,
            default=SUPPRESS,
            required=True,
            help="Provide machine_type_id to create-machine-conf."
        )
        create_machine_conf.add_argument(
            "--is_spot_instance",
            type=str,
            default='false',
            nargs='?',
            metavar='true,false',
            help="Provide is_spot_instance to create-machine-conf."
        )
        create_machine_conf.add_argument(
            "--enable_public_ip",
            type=str,
            default='false',
            nargs='?',
            metavar='true,false',
            help="Provide enable_public_ip to create-machine-conf."
        )
        create_machine_conf.add_argument(
            "--block_project_ssh_keys",
            type=str,
            default='true',
            nargs='?',
            metavar='true,false',
            help="Provide block_project_ssh_keys to create-machine-conf."
        )
        create_machine_conf.add_argument(
            "--bootstrap_shell_script_file_path",
            type=str,
            default=SUPPRESS,
            nargs=1,
            help="Provide bootstrap_shell_script_file_path to create-machine-conf."
        )
        create_machine_conf.add_argument(
            "--network_conf_id",
            type=int,
            nargs=1,
            default=SUPPRESS,
            required=True,
            help="Provide network_conf_id to create-machine-conf."
        )
        create_machine_conf.add_argument(
            "--volume_conf_id",
            type=int,
            nargs=1,
            default=SUPPRESS,
            required=True,
            help="Provide volume_conf_id to create-machine-conf."
        )
        create_machine_conf.add_argument(
            "--json-output",
            type=str,
            nargs='?',
            choices=['pretty', 'default'],
            default='pretty',
            help="Provide the format of JSON output."
        )
        create_machine_conf.add_argument(
            "--yaml-output",
            type=str,
            nargs='?',
            choices=['true', 'false'],
            default='false',
            help="Provide true to get output in YAML format."
        )

        describe_machine_conf = subparser.add_parser(
            'get-machine-conf',
            help='To get information about a specific Machine Configuration.',
            formatter_class=ArgumentDefaultsHelpFormatter)
        describe_machine_conf.add_argument(
            "--machine_conf_id",
            type=int,
            nargs=1,
            default=SUPPRESS,
            required=True,
            help="Provide machine config id to get information about a specific Machine Configuration."
        )
        describe_machine_conf.add_argument(
            "--json-output",
            type=str,
            nargs='?',
            choices=['pretty', 'default'],
            default='pretty',
            help="Provide the format of JSON output."
        )
        describe_machine_conf.add_argument(
            "--yaml-output",
            type=str,
            nargs='?',
            choices=['true', 'false'],
            default='false',
            help="Provide true to get output in YAML format."
        )

        list_machine_conf = subparser.add_parser(
            'list-machine-confs',
            help='To list all the available Machine Configurations.',
            formatter_class=ArgumentDefaultsHelpFormatter)
        list_machine_conf.add_argument(
            "--cloud_provider",
            type=str,
            nargs='?',
            default=SUPPRESS,
            choices=CLOUD_PROVIDERS_LIST,
            help="Cloud Provider that will be used for filtering list."
        )
        list_machine_conf.add_argument(
            "--json-output",
            type=str,
            nargs='?',
            choices=['pretty', 'default'],
            default='pretty',
            help="Provide the format of JSON output."
        )
        list_machine_conf.add_argument(
            "--yaml-output",
            type=str,
            nargs='?',
            choices=['true', 'false'],
            default='false',
            help="Provide true to get output in YAML format."
        )

        edit_machine_conf = subparser.add_parser(
            'edit-machine-conf',
            help='To edit a specific Machine Configuration.',
            formatter_class=ArgumentDefaultsHelpFormatter)
        edit_machine_conf.add_argument(
            "--machine_conf_id",
            type=int,
            nargs=1,
            default=SUPPRESS,
            required=True,
            help="Provide a specific machine configuration id to edit-machine-conf."
        )
        edit_machine_conf.add_argument(
            "--network_tags",
            type=str,
            default=SUPPRESS,
            metavar=['value1,value2'],
            help="Provide network_tags to edit-machine-conf."
        )
        edit_machine_conf.add_argument(
            "--labels",
            type=str,
            action='append',
            nargs='+',
            default=SUPPRESS,
            help="Provide labels to edit-machine-conf."
        )
        edit_machine_conf.add_argument(
            "--service_account_instance_profile",
            type=str,
            nargs='?',
            default=SUPPRESS,
            help="Provide service_account_instance_profile to edit-machine-conf."
        )
        edit_machine_conf.add_argument(
            "--is_spot_instance",
            type=str,
            nargs='?',
            default=SUPPRESS,
            metavar='true,false',
            help="Provide is_spot_instance to edit-machine-conf."
        )
        edit_machine_conf.add_argument(
            "--enable_public_ip",
            type=str,
            nargs='?',
            default=SUPPRESS,
            metavar='true,false',
            help="Provide enable_public_ip to edit-machine-conf."
        )
        edit_machine_conf.add_argument(
            "--block_project_ssh_keys",
            type=str,
            nargs='?',
            default=SUPPRESS,
            metavar='true,false',
            help="Provide block_project_ssh_keys to edit-machine-conf."
        )
        edit_machine_conf.add_argument(
            "--bootstrap_shell_script_file_path",
            type=str,
            default=SUPPRESS,
            nargs='?',
            help="Provide bootstrap_shell_script_file_path to edit-machine-conf."
        )
        edit_machine_conf.add_argument(
            "--json-output",
            type=str,
            nargs='?',
            choices=['pretty', 'default'],
            default='pretty',
            help="Provide the format of JSON output."
        )
        edit_machine_conf.add_argument(
            "--yaml-output",
            type=str,
            nargs='?',
            choices=['true', 'false'],
            default='false',
            help="Provide true to get output in YAML format."
        )
