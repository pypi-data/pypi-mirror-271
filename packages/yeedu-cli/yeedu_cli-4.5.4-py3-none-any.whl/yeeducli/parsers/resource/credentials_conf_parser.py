from yeeducli.constants import CLOUD_PROVIDERS_LIST
from argparse import SUPPRESS, ArgumentDefaultsHelpFormatter


class CredentialsConfigurationParser:

    def credentials_config_parser(subparser):
        create_credentials_conf = subparser.add_parser(
            'create-credential-conf',
            help='To create a Credential Configuration.',
            formatter_class=ArgumentDefaultsHelpFormatter)
        create_credentials_conf.add_argument(
            "--credential_type_id",
            type=int,
            nargs=1,
            default=SUPPRESS,
            required=True,
            help="Provide credential_type_id to create-credential-conf."
        )
        create_credentials_conf.add_argument(
            "--base64_encoded_credentials",
            type=str,
            nargs=1,
            default=SUPPRESS,
            required=True,
            help="Provide base64_encoded_credentials to create-credential-conf."
        )
        create_credentials_conf.add_argument(
            "--name",
            type=str,
            nargs=1,
            default=SUPPRESS,
            required=True,
            help="Provide name to create-credential-conf."
        )
        create_credentials_conf.add_argument(
            "--json-output",
            type=str,
            nargs='?',
            choices=['pretty', 'default'],
            default='pretty',
            help="Provide the format of JSON output."
        )
        create_credentials_conf.add_argument(
            "--yaml-output",
            type=str,
            nargs='?',
            choices=['true', 'false'],
            default='false',
            help="Provide true to get output in YAML format."
        )

        list_credentials_conf = subparser.add_parser(
            'list-credential-confs',
            help='To list all the available Credential Configurations.',
            formatter_class=ArgumentDefaultsHelpFormatter)
        list_credentials_conf.add_argument(
            "--cloud_provider",
            type=str,
            nargs='?',
            default=SUPPRESS,
            choices=CLOUD_PROVIDERS_LIST,
            help="Cloud Provider that will be used for filtering list."
        )
        list_credentials_conf.add_argument(
            "--json-output",
            type=str,
            nargs='?',
            choices=['pretty', 'default'],
            default='pretty',
            help="Provide the format of JSON output."
        )
        list_credentials_conf.add_argument(
            "--yaml-output",
            type=str,
            nargs='?',
            choices=['true', 'false'],
            default='false',
            help="Provide true to get output in YAML format."
        )

        describe_credentials_conf = subparser.add_parser(
            'get-credential-conf',
            help='To get the information about a specific Credential Configuration.',
            formatter_class=ArgumentDefaultsHelpFormatter)
        describe_credentials_conf.add_argument(
            "--credentials_conf_id",
            type=int,
            nargs=1,
            default=SUPPRESS,
            required=True,
            help="Provide credentials_conf_id to get information about a specific credential configuration."
        )
        describe_credentials_conf.add_argument(
            "--json-output",
            type=str,
            nargs='?',
            choices=['pretty', 'default'],
            default='pretty',
            help="Provide the format of JSON output."
        )
        describe_credentials_conf.add_argument(
            "--yaml-output",
            type=str,
            nargs='?',
            choices=['true', 'false'],
            default='false',
            help="Provide true to get output in YAML format."
        )

        edit_credentials_conf = subparser.add_parser(
            'edit-credential-conf',
            help='To edit a specific Credential Configuration.',
            formatter_class=ArgumentDefaultsHelpFormatter)
        edit_credentials_conf.add_argument(
            "--credentials_conf_id",
            type=int,
            nargs=1,
            default=SUPPRESS,
            required=True,
            help="Provide a specific credentials cofig id to edit-credential-conf."
        )
        edit_credentials_conf.add_argument(
            "--base64_encoded_credentials",
            type=str,
            nargs=1,
            default=SUPPRESS,
            help="Provide base64_encoded_credentials to edit-credential-conf."
        )
        edit_credentials_conf.add_argument(
            "--name",
            type=str,
            nargs='?',
            default=SUPPRESS,
            help="Provide name to edit-credential-conf."
        )
        edit_credentials_conf.add_argument(
            "--json-output",
            type=str,
            nargs='?',
            choices=['pretty', 'default'],
            default='pretty',
            help="Provide the format of JSON output."
        )
        edit_credentials_conf.add_argument(
            "--yaml-output",
            type=str,
            nargs='?',
            choices=['true', 'false'],
            default='false',
            help="Provide true to get output in YAML format."
        )

        delete_credentials_conf = subparser.add_parser(
            'delete-credential-conf',
            help='To delete a specific Credential Configuration.',
            formatter_class=ArgumentDefaultsHelpFormatter)
        delete_credentials_conf.add_argument(
            "--credentials_conf_id",
            type=int,
            nargs=1,
            default=SUPPRESS,
            required=True,
            help="Provide credentials_conf_id to delete a specific Credential Configuration."
        )
        delete_credentials_conf.add_argument(
            "--json-output",
            type=str,
            nargs='?',
            choices=['pretty', 'default'],
            default='pretty',
            help="Provide the format of JSON output."
        )
        delete_credentials_conf.add_argument(
            "--yaml-output",
            type=str,
            nargs='?',
            choices=['true', 'false'],
            default='false',
            help="Provide true to get output in YAML format."
        )

