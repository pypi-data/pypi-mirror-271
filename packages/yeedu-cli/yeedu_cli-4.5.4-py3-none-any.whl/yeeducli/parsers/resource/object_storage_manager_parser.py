from yeeducli.constants import CLOUD_PROVIDERS_LIST
from argparse import SUPPRESS, ArgumentDefaultsHelpFormatter


class ObjectStorageManagerParser:

    def object_storage_manager_parser(subparser):
        create_object_storage_manager_conf = subparser.add_parser(
            'create-object-storage-manager',
            help='To create a Object Storage Manager.',
            formatter_class=ArgumentDefaultsHelpFormatter)
        create_object_storage_manager_conf.add_argument(
            "--name",
            type=str,
            nargs=1,
            default=SUPPRESS,
            required=True,
            help="Provide name to create-object-storage-manager."
        )
        create_object_storage_manager_conf.add_argument(
            "--credentials_conf_id",
            type=int,
            nargs=1,
            default=SUPPRESS,
            required=True,
            help="Provide credentials_conf_id to create-object-storage-manager."
        )
        create_object_storage_manager_conf.add_argument(
            "--object_storage_bucket_name",
            type=str,
            nargs=1,
            default=SUPPRESS,
            required=True,
            help="Provide object_storage_bucket_name to create-object-storage-manager."
        )
        create_object_storage_manager_conf.add_argument(
            "--json-output",
            type=str,
            nargs='?',
            choices=['pretty', 'default'],
            default='pretty',
            help="Provide the format of JSON output."
        )
        create_object_storage_manager_conf.add_argument(
            "--yaml-output",
            type=str,
            nargs='?',
            choices=['true', 'false'],
            default='false',
            help="Provide true to get output in YAML format."
        )

        describe_object_storage_manager_conf = subparser.add_parser(
            'get-object-storage-manager',
            help='To get information about a specific Object Storage Manager.',
            formatter_class=ArgumentDefaultsHelpFormatter)
        describe_object_storage_manager_conf.add_argument(
            "--object_storage_manager_id",
            type=int,
            nargs=1,
            default=SUPPRESS,
            required=True,
            help="Provide Object Storage Manager Id to get information about a specific Object Storage Manager."
        )
        describe_object_storage_manager_conf.add_argument(
            "--json-output",
            type=str,
            nargs='?',
            choices=['pretty', 'default'],
            default='pretty',
            help="Provide the format of JSON output."
        )
        describe_object_storage_manager_conf.add_argument(
            "--yaml-output",
            type=str,
            nargs='?',
            choices=['true', 'false'],
            default='false',
            help="Provide true to get output in YAML format."
        )

        list_object_storage_manager_conf = subparser.add_parser(
            'list-object-storage-managers',
            help='To list all the available  Object Storage Manager Configurations.',
            formatter_class=ArgumentDefaultsHelpFormatter)
        list_object_storage_manager_conf.add_argument(
            "--cloud_provider",
            type=str,
            nargs='?',
            default=SUPPRESS,
            choices=CLOUD_PROVIDERS_LIST,
            help="Cloud Provider that will be used for filtering list."
        )
        list_object_storage_manager_conf.add_argument(
            "--json-output",
            type=str,
            nargs='?',
            choices=['pretty', 'default'],
            default='pretty',
            help="Provide the format of JSON output."
        )
        list_object_storage_manager_conf.add_argument(
            "--yaml-output",
            type=str,
            nargs='?',
            choices=['true', 'false'],
            default='false',
            help="Provide true to get output in YAML format."
        )

        edit_object_storage_manager_conf = subparser.add_parser(
            'edit-object-storage-manager',
            help='To edit a specific Object Storage Manager Configuration.',
            formatter_class=ArgumentDefaultsHelpFormatter)
        edit_object_storage_manager_conf.add_argument(
            "--object_storage_manager_id",
            type=int,
            nargs=1,
            default=SUPPRESS,
            required=True,
            help="Provide object_storage_manager_id to edit information about a specific Object Storage Manager."
        )
        edit_object_storage_manager_conf.add_argument(
            "--name",
            type=str,
            nargs=1,
            default=SUPPRESS,
            help="Provide name to edit-object-storage-manager."
        )
        edit_object_storage_manager_conf.add_argument(
            "--object_storage_bucket_name",
            type=str,
            nargs='?',
            default=SUPPRESS,
            help="Provide object_storage_bucket_name to edit-object-storage-manager."
        )
        edit_object_storage_manager_conf.add_argument(
            "--json-output",
            type=str,
            nargs='?',
            choices=['pretty', 'default'],
            default='pretty',
            help="Provide the format of JSON output."
        )
        edit_object_storage_manager_conf.add_argument(
            "--yaml-output",
            type=str,
            nargs='?',
            choices=['true', 'false'],
            default='false',
            help="Provide true to get output in YAML format."
        )

        delete_object_storage_manager_conf = subparser.add_parser(
            'delete-object-storage-manager',
            help='To delete a specific Object Storage Manager.',
            formatter_class=ArgumentDefaultsHelpFormatter)
        delete_object_storage_manager_conf.add_argument(
            "--object_storage_manager_id",
            type=int,
            nargs=1,
            default=SUPPRESS,
            required=True,
            help="Provide object_storage_manager_id to delete a specific Object Storage Manager."
        )
        delete_object_storage_manager_conf.add_argument(
            "--json-output",
            type=str,
            nargs='?',
            choices=['pretty', 'default'],
            default='pretty',
            help="Provide the format of JSON output."
        )
        delete_object_storage_manager_conf.add_argument(
            "--yaml-output",
            type=str,
            nargs='?',
            choices=['true', 'false'],
            default='false',
            help="Provide true to get output in YAML format."
        )
