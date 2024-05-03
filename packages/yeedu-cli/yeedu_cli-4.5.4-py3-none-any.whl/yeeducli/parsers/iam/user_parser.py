from argparse import ArgumentDefaultsHelpFormatter, SUPPRESS


class UserParser:

    # 'list-tenants', 'associate-tenant', 'get-user-info', 'get-user-roles',
    def user_parser(subparser):

        list_tenants = subparser.add_parser(
            'list-tenants',
            help='To list all the available tenants for the session user.',
            formatter_class=ArgumentDefaultsHelpFormatter)
        list_tenants.add_argument(
            "--json-output",
            type=str,
            nargs='?',
            choices=['pretty', 'default'],
            default='pretty',
            help="Provide the format of JSON output."
        )
        list_tenants.add_argument(
            "--yaml-output",
            type=str,
            nargs='?',
            choices=['true', 'false'],
            default='false',
            help="Provide true to get output in YAML format."
        )

        associate_tenant = subparser.add_parser(
            'associate-tenant',
            help='To associate tenant with the current users session token.',
            formatter_class=ArgumentDefaultsHelpFormatter)
        associate_tenant.add_argument(
            "--tenant_id",
            type=str,
            nargs=1,
            required=True,
            default=SUPPRESS,
            help="Provide tenant_id to associate it with session token"
        )
        associate_tenant.add_argument(
            "--json-output",
            type=str,
            nargs='?',
            choices=['pretty', 'default'],
            default='pretty',
            help="Provide the format of JSON output."
        )
        associate_tenant.add_argument(
            "--yaml-output",
            type=str,
            nargs='?',
            choices=['true', 'false'],
            default='false',
            help="Provide true to get output in YAML format."
        )

        get_user_info = subparser.add_parser(
            'get-user-info',
            help='To get information about current session user.',
            formatter_class=ArgumentDefaultsHelpFormatter)
        get_user_info.add_argument(
            "--json-output",
            type=str,
            nargs='?',
            choices=['pretty', 'default'],
            default='pretty',
            help="Provide the format of JSON output."
        )
        get_user_info.add_argument(
            "--yaml-output",
            type=str,
            nargs='?',
            choices=['true', 'false'],
            default='false',
            help="Provide true to get output in YAML format."
        )

        get_user_roles = subparser.add_parser(
            'get-user-roles',
            help='To get all the roles of current session user.',
            formatter_class=ArgumentDefaultsHelpFormatter)
        get_user_roles.add_argument(
            "--json-output",
            type=str,
            nargs='?',
            choices=['pretty', 'default'],
            default='pretty',
            help="Provide the format of JSON output."
        )
        get_user_roles.add_argument(
            "--yaml-output",
            type=str,
            nargs='?',
            choices=['true', 'false'],
            default='false',
            help="Provide true to get output in YAML format."
        )
