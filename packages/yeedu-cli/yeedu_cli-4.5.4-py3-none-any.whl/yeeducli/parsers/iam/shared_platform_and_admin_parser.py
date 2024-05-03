from argparse import SUPPRESS, ArgumentDefaultsHelpFormatter


class SharedPlatformAndAdminParser:

    def shared_platform_and_admin_parser(subparser):

        sync_user = subparser.add_parser(
            'sync-user',
            help='To get the information about a specific User.',
            formatter_class=ArgumentDefaultsHelpFormatter)
        sync_user.add_argument(
            "--username",
            type=str,
            nargs=1,
            default=SUPPRESS,
            required=True,
            help="Provide username to get information about a specific User."
        )
        sync_user.add_argument(
            "--json-output",
            type=str,
            nargs='?',
            choices=['pretty', 'default'],
            default='pretty',
            help="Provide the format of JSON output."
        )
        sync_user.add_argument(
            "--yaml-output",
            type=str,
            nargs='?',
            choices=['true', 'false'],
            default='false',
            help="Provide true to get output in YAML format."
        )

        sync_group = subparser.add_parser(
            'sync-group',
            help='To get the information about a specific Group.',
            formatter_class=ArgumentDefaultsHelpFormatter)
        sync_group.add_argument(
            "--groupname",
            type=str,
            nargs=1,
            default=SUPPRESS,
            required=True,
            help="Provide groupname to get information about a specific Group."
        )
        sync_group.add_argument(
            "--json-output",
            type=str,
            nargs='?',
            choices=['pretty', 'default'],
            default='pretty',
            help="Provide the format of JSON output."
        )
        sync_group.add_argument(
            "--yaml-output",
            type=str,
            nargs='?',
            choices=['true', 'false'],
            default='false',
            help="Provide true to get output in YAML format."
        )

        list_user_groups = subparser.add_parser(
            'list-user-groups',
            help='To list all the Groups for a specific User.',
            formatter_class=ArgumentDefaultsHelpFormatter)
        list_user_groups.add_argument(
            "--user_id",
            type=int,
            nargs=1,
            default=SUPPRESS,
            required=True,
            help="Provide user_id to list all the Groups for a specific User."
        )
        list_user_groups.add_argument(
            "--json-output",
            type=str,
            nargs='?',
            choices=['pretty', 'default'],
            default='pretty',
            help="Provide the format of JSON output."
        )
        list_user_groups.add_argument(
            "--yaml-output",
            type=str,
            nargs='?',
            choices=['true', 'false'],
            default='false',
            help="Provide true to get output in YAML format."
        )

        list_users = subparser.add_parser(
            'list-users',
            help='To list all the available Users.',
            formatter_class=ArgumentDefaultsHelpFormatter)
        list_users.add_argument(
            "--json-output",
            type=str,
            nargs='?',
            choices=['pretty', 'default'],
            default='pretty',
            help="Provide the format of JSON output."
        )
        list_users.add_argument(
            "--yaml-output",
            type=str,
            nargs='?',
            choices=['true', 'false'],
            default='false',
            help="Provide true to get output in YAML format."
        )

        list_group_users = subparser.add_parser(
            'list-group-users',
            help='To list all the Users for a specific Group.',
            formatter_class=ArgumentDefaultsHelpFormatter)
        list_group_users.add_argument(
            "--group_id",
            type=int,
            nargs=1,
            default=SUPPRESS,
            required=True,
            help="Provide group_id to list all the Users for a specific Group."
        )
        list_group_users.add_argument(
            "--json-output",
            type=str,
            nargs='?',
            choices=['pretty', 'default'],
            default='pretty',
            help="Provide the format of JSON output."
        )
        list_group_users.add_argument(
            "--yaml-output",
            type=str,
            nargs='?',
            choices=['true', 'false'],
            default='false',
            help="Provide true to get output in YAML format."
        )

        list_groups = subparser.add_parser(
            'list-groups',
            help='To list all the available Groups.',
            formatter_class=ArgumentDefaultsHelpFormatter)
        list_groups.add_argument(
            "--json-output",
            type=str,
            nargs='?',
            choices=['pretty', 'default'],
            default='pretty',
            help="Provide the format of JSON output."
        )
        list_groups.add_argument(
            "--yaml-output",
            type=str,
            nargs='?',
            choices=['true', 'false'],
            default='false',
            help="Provide true to get output in YAML format."
        )

        search_users = subparser.add_parser(
            'search-user',
            help='To search the users based on username.',
            formatter_class=ArgumentDefaultsHelpFormatter)
        search_users.add_argument(
            "--username",
            type=str,
            nargs=1,
            default=SUPPRESS,
            required=True,
            help="Provide username to get information about a specific User."
        )
        search_users.add_argument(
            "--json-output",
            type=str,
            nargs='?',
            choices=['pretty', 'default'],
            default='pretty',
            help="Provide the format of JSON output."
        )
        search_users.add_argument(
            "--yaml-output",
            type=str,
            nargs='?',
            choices=['true', 'false'],
            default='false',
            help="Provide true to get output in YAML format."
        )

        search_groups = subparser.add_parser(
            'search-group',
            help='To search the groups based on groupname.',
            formatter_class=ArgumentDefaultsHelpFormatter)
        search_groups.add_argument(
            "--groupname",
            type=str,
            nargs=1,
            default=SUPPRESS,
            required=True,
            help="Provide groupname to get information about a specific Group."
        )
        search_groups.add_argument(
            "--json-output",
            type=str,
            nargs='?',
            choices=['pretty', 'default'],
            default='pretty',
            help="Provide the format of JSON output."
        )
        search_groups.add_argument(
            "--yaml-output",
            type=str,
            nargs='?',
            choices=['true', 'false'],
            default='false',
            help="Provide true to get output in YAML format."
        )