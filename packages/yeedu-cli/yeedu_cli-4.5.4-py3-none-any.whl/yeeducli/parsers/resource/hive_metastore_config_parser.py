from argparse import SUPPRESS, ArgumentDefaultsHelpFormatter


class HiveMetastoreConfigParser:

    def hive_metastore_config_parser(subparser):
        create_hive_metastore_config = subparser.add_parser(
            'create-hive-metastore-conf',
            help='To create a Hive Metastore Configuration.',
            formatter_class=ArgumentDefaultsHelpFormatter)
        create_hive_metastore_config.add_argument(
            "--hive_site_xml_file_path",
            type=str,
            nargs=1,
            default=SUPPRESS,
            help="Provide hive_site_xml_file_path to create-hive-metastore-conf."
        )
        create_hive_metastore_config.add_argument(
            "--core_site_xml_file_path",
            type=str,
            nargs=1,
            default=SUPPRESS,
            help="Provide core_site_xml_file_path to create-hive-metastore-conf."
        )
        create_hive_metastore_config.add_argument(
            "--hdfs_site_xml_file_path",
            type=str,
            nargs=1,
            default=SUPPRESS,
            help="Provide hdfs_site_xml_file_path to create-hive-metastore-conf."
        )
        create_hive_metastore_config.add_argument(
            "--krb5_conf_file_path",
            type=str,
            nargs=1,
            default=SUPPRESS,
            help="Provide krb5_conf_file_path to create-hive-metastore-conf."
        )
        create_hive_metastore_config.add_argument(
            "--json-output",
            type=str,
            nargs='?',
            choices=['pretty', 'default'],
            default='pretty',
            help="Provide the format of JSON output."
        )
        create_hive_metastore_config.add_argument(
            "--yaml-output",
            type=str,
            nargs='?',
            choices=['true', 'false'],
            default='false',
            help="Provide true to get output in YAML format."
        )

        list_hive_metastore_config = subparser.add_parser(
            'list-hive-metastore-confs',
            help='To list all the available Hive Metastore Configurations.',
            formatter_class=ArgumentDefaultsHelpFormatter)
        list_hive_metastore_config.add_argument(
            "--json-output",
            type=str,
            nargs='?',
            choices=['pretty', 'default'],
            default='pretty',
            help="Provide the format of JSON output."
        )
        list_hive_metastore_config.add_argument(
            "--yaml-output",
            type=str,
            nargs='?',
            choices=['true', 'false'],
            default='false',
            help="Provide true to get output in YAML format."
        )

        describe_hive_metastore_config = subparser.add_parser(
            'get-hive-metastore-conf',
            help='To get the information about a specific Hive Metastore Configuration.',
            formatter_class=ArgumentDefaultsHelpFormatter)
        describe_hive_metastore_config.add_argument(
            "--hive_metastore_conf_id",
            type=int,
            nargs=1,
            default=SUPPRESS,
            required=True,
            help="Provide hive_metastore_conf_id to get information about a specific Hive Metastore Configuration."
        )
        describe_hive_metastore_config.add_argument(
            "--json-output",
            type=str,
            nargs='?',
            choices=['pretty', 'default'],
            default='pretty',
            help="Provide the format of JSON output."
        )
        describe_hive_metastore_config.add_argument(
            "--yaml-output",
            type=str,
            nargs='?',
            choices=['true', 'false'],
            default='false',
            help="Provide true to get output in YAML format."
        )

        edit_hive_metastore_config = subparser.add_parser(
            'edit-hive-metastore-conf',
            help='To edit a specific Hive Metastore Configuration.',
            formatter_class=ArgumentDefaultsHelpFormatter)
        edit_hive_metastore_config.add_argument(
            "--hive_metastore_conf_id",
            type=int,
            nargs=1,
            default=SUPPRESS,
            required=True,
            help="Provide a specific hive_metastore_conf_id to edit-hive-metastore-conf."
        )
        edit_hive_metastore_config.add_argument(
            "--hive_site_xml_file_path",
            type=str,
            nargs=1,
            default=SUPPRESS,
            help="Provide hive_site_xml_file_path to edit-hive-metastore-conf."
        )
        edit_hive_metastore_config.add_argument(
            "--core_site_xml_file_path",
            type=str,
            nargs=1,
            default=SUPPRESS,
            help="Provide core_site_xml_file_path to edit-hive-metastore-conf."
        )
        edit_hive_metastore_config.add_argument(
            "--hdfs_site_xml_file_path",
            type=str,
            nargs=1,
            default=SUPPRESS,
            help="Provide hdfs_site_xml_file_path to edit-hive-metastore-conf."
        )
        edit_hive_metastore_config.add_argument(
            "--krb5_conf_file_path",
            type=str,
            nargs=1,
            default=SUPPRESS,
            help="Provide krb5_conf_file_path to edit-hive-metastore-conf."
        )
        edit_hive_metastore_config.add_argument(
            "--json-output",
            type=str,
            nargs='?',
            choices=['pretty', 'default'],
            default='pretty',
            help="Provide the format of JSON output."
        )
        edit_hive_metastore_config.add_argument(
            "--yaml-output",
            type=str,
            nargs='?',
            choices=['true', 'false'],
            default='false',
            help="Provide true to get output in YAML format."
        )

        delete_hive_metastore_config = subparser.add_parser(
            'delete-hive-metastore-conf',
            help='To delete a specific Hive Metastore Configuration.',
            formatter_class=ArgumentDefaultsHelpFormatter)
        delete_hive_metastore_config.add_argument(
            "--hive_metastore_conf_id",
            type=int,
            nargs=1,
            default=SUPPRESS,
            required=True,
            help="Provide hive_metastore_conf_id to delete a specific Hive Metastore Configuration."
        )
        delete_hive_metastore_config.add_argument(
            "--json-output",
            type=str,
            nargs='?',
            choices=['pretty', 'default'],
            default='pretty',
            help="Provide the format of JSON output."
        )
        delete_hive_metastore_config.add_argument(
            "--yaml-output",
            type=str,
            nargs='?',
            choices=['true', 'false'],
            default='false',
            help="Provide true to get output in YAML format."
        )
