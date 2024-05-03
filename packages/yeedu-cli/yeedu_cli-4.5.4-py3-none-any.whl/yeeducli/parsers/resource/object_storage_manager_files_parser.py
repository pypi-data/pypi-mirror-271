from argparse import SUPPRESS, ArgumentDefaultsHelpFormatter


class ObjectStorageManagerFilesParser:

    def object_storage_manager_files_parser(subparser):
        create_object_storage_manager_files = subparser.add_parser(
            'create-object-storage-manager-file',
            help='To create a Object Storage Manager Files.',
            formatter_class=ArgumentDefaultsHelpFormatter)
        create_object_storage_manager_files.add_argument(
            "--object_storage_manager_id",
            type=int,
            nargs=1,
            default=SUPPRESS,
            required=True,
            help="Provide credential_fileig_id to create-object-storage-manager-file."
        )
        create_object_storage_manager_files.add_argument(
            "--local_file_path",
            type=str,
            nargs=1,
            default=SUPPRESS,
            required=True,
            help="Provide local_file_path to create-object-storage-manager-file."
        )
        create_object_storage_manager_files.add_argument(
            "--preserve_path",
            type=str,
            nargs='?',
            choices=['true', 'false'],
            default='false',
            help="Provide preserve_path to create-object-storage-manager-file."
        )
        create_object_storage_manager_files.add_argument(
            "--overwrite",
            type=str,
            nargs='?',
            choices=['true', 'false'],
            default='false',
            help="Provide overwrite to create-object-storage-manager-file."
        )
        create_object_storage_manager_files.add_argument(
            "--json-output",
            type=str,
            nargs='?',
            choices=['pretty', 'default'],
            default='pretty',
            help="Provide the format of JSON output."
        )
        create_object_storage_manager_files.add_argument(
            "--yaml-output",
            type=str,
            nargs='?',
            choices=['true', 'false'],
            default='false',
            help="Provide true to get output in YAML format."
        )

        list_object_storage_manager_files = subparser.add_parser(
            'list-object-storage-manager-files',
            help='To list all the available Object Storage Manager Files.',
            formatter_class=ArgumentDefaultsHelpFormatter)
        list_object_storage_manager_files.add_argument(
            "--object_storage_manager_id",
            type=int,
            nargs=1,
            default=SUPPRESS,
            required=True,
            help="Provide Object Storage Manager Id to list all the available Object Storage Manager Files."
        )
        list_object_storage_manager_files.add_argument(
            "--json-output",
            type=str,
            nargs='?',
            choices=['pretty', 'default'],
            default='pretty',
            help="Provide the format of JSON output."
        )
        list_object_storage_manager_files.add_argument(
            "--yaml-output",
            type=str,
            nargs='?',
            choices=['true', 'false'],
            default='false',
            help="Provide true to get output in YAML format."
        )

        describe_object_storage_manager_files = subparser.add_parser(
            'get-object-storage-manager-file',
            help='To get information about a specific Object Storage Manager File.',
            formatter_class=ArgumentDefaultsHelpFormatter)
        describe_object_storage_manager_files.add_argument(
            "--object_storage_manager_id",
            type=int,
            nargs=1,
            default=SUPPRESS,
            required=True,
            help="Provide Object Storage Manager Id to get information about a specific Object Storage Manager Files."
        )
        describe_object_storage_manager_files.add_argument(
            "--file_id",
            type=int,
            nargs=1,
            default=SUPPRESS,
            required=True,
            help="Provide File Id to get information about a specific Object Storage Manager Files."
        )
        describe_object_storage_manager_files.add_argument(
            "--json-output",
            type=str,
            nargs='?',
            choices=['pretty', 'default'],
            default='pretty',
            help="Provide the format of JSON output."
        )
        describe_object_storage_manager_files.add_argument(
            "--yaml-output",
            type=str,
            nargs='?',
            choices=['true', 'false'],
            default='false',
            help="Provide true to get output in YAML format."
        )

        delete_object_storage_manager_files = subparser.add_parser(
            'delete-object-storage-manager-file',
            help='To delete a specific Object Storage Manager File.',
            formatter_class=ArgumentDefaultsHelpFormatter)
        delete_object_storage_manager_files.add_argument(
            "--object_storage_manager_id",
            type=int,
            nargs=1,
            default=SUPPRESS,
            required=True,
            help="Provide Object Storage Manager Id to delete a specific Object Storage Manager File."
        )
        delete_object_storage_manager_files.add_argument(
            "--file_id",
            type=int,
            nargs=1,
            default=SUPPRESS,
            required=True,
            help="Provide File Id to delete a specific Object Storage Manager Files."
        )
        delete_object_storage_manager_files.add_argument(
            "--json-output",
            type=str,
            nargs='?',
            choices=['pretty', 'default'],
            default='pretty',
            help="Provide the format of JSON output."
        )
        delete_object_storage_manager_files.add_argument(
            "--yaml-output",
            type=str,
            nargs='?',
            choices=['true', 'false'],
            default='false',
            help="Provide true to get output in YAML format."
        )
