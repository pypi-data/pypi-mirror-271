from argparse import SUPPRESS, ArgumentDefaultsHelpFormatter


class CommonPlatformAndAdminParser:

    def admin_parser(subparser):
        list_users = subparser.add_parser(
            'list-users',
            help='To list all the users present in tenant.',
            formatter_class=ArgumentDefaultsHelpFormatter)
        list_users.add_argument(
            "--page_number",
            type=int,
            nargs=1,
            default=1,
            help="To list users for a specific page_number."
        )
        list_users.add_argument(
            "--limit",
            type=int,
            nargs=1,
            default=100,
            help="Provide limit to list number of users."
        )
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

        get_user = subparser.add_parser(
            'get-user',
            help='To get information about a specific User.',
            formatter_class=ArgumentDefaultsHelpFormatter)
        get_user.add_argument(
            "--user_id",
            type=int,
            nargs=1,
            default=SUPPRESS,
            required=True,
            help="Provide User Id to get information about a specific User."
        )
        get_user.add_argument(
            "--json-output",
            type=str,
            nargs='?',
            choices=['pretty', 'default'],
            default='pretty',
            help="Provide the format of JSON output."
        )
        get_user.add_argument(
            "--yaml-output",
            type=str,
            nargs='?',
            choices=['true', 'false'],
            default='false',
            help="Provide true to get output in YAML format."
        )

        get_user_roles = subparser.add_parser(
            'get-user-roles',
            help='To get all the roles of a specific User.',
            formatter_class=ArgumentDefaultsHelpFormatter)
        get_user_roles.add_argument(
            "--user_id",
            type=int,
            nargs=1,
            default=SUPPRESS,
            required=True,
            help="Provide User Id to get roles of a specific User."
        )
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

        list_user_roles = subparser.add_parser(
            'list-users-roles',
            help='To list all the Users Roles.',
            formatter_class=ArgumentDefaultsHelpFormatter)
        list_user_roles.add_argument(
            "--page_number",
            type=int,
            nargs=1,
            default=1,
            help="To list users roles for a specific page_number."
        )
        list_user_roles.add_argument(
            "--limit",
            type=int,
            nargs=1,
            default=100,
            help="Provide limit to list number of users roles."
        )
        list_user_roles.add_argument(
            "--json-output",
            type=str,
            nargs='?',
            choices=['pretty', 'default'],
            default='pretty',
            help="Provide the format of JSON output."
        )
        list_user_roles.add_argument(
            "--yaml-output",
            type=str,
            nargs='?',
            choices=['true', 'false'],
            default='false',
            help="Provide true to get output in YAML format."
        )

        get_role_users = subparser.add_parser(
            'get-role-users',
            help='To get all the users in a specific Role.',
            formatter_class=ArgumentDefaultsHelpFormatter)
        get_role_users.add_argument(
            "--role_id",
            type=int,
            nargs=1,
            default=SUPPRESS,
            required=True,
            help="Provide Role Id to get users in a specific Role."
        )
        get_role_users.add_argument(
            "--json-output",
            type=str,
            nargs='?',
            choices=['pretty', 'default'],
            default='pretty',
            help="Provide the format of JSON output."
        )
        get_role_users.add_argument(
            "--yaml-output",
            type=str,
            nargs='?',
            choices=['true', 'false'],
            default='false',
            help="Provide true to get output in YAML format."
        )

        list_groups = subparser.add_parser(
            'list-groups',
            help='To list all the groups present in tenant.',
            formatter_class=ArgumentDefaultsHelpFormatter)
        list_groups.add_argument(
            "--page_number",
            type=int,
            nargs=1,
            default=1,
            help="To list groups for a specific page_number."
        )
        list_groups.add_argument(
            "--limit",
            type=int,
            nargs=1,
            default=100,
            help="Provide limit to list number of groups."
        )
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

        get_group = subparser.add_parser(
            'get-group',
            help='To get information about a specific Group.',
            formatter_class=ArgumentDefaultsHelpFormatter)
        get_group.add_argument(
            "--group_id",
            type=int,
            nargs=1,
            default=SUPPRESS,
            required=True,
            help="Provide Group Id to get information about a specific Group."
        )
        get_group.add_argument(
            "--json-output",
            type=str,
            nargs='?',
            choices=['pretty', 'default'],
            default='pretty',
            help="Provide the format of JSON output."
        )
        get_group.add_argument(
            "--yaml-output",
            type=str,
            nargs='?',
            choices=['true', 'false'],
            default='false',
            help="Provide true to get output in YAML format."
        )

        get_group_roles = subparser.add_parser(
            'get-group-roles',
            help='To get all the roles of a specific Group.',
            formatter_class=ArgumentDefaultsHelpFormatter)
        get_group_roles.add_argument(
            "--group_id",
            type=int,
            nargs=1,
            default=SUPPRESS,
            required=True,
            help="Provide Group Id to get roles of a specific Group."
        )
        get_group_roles.add_argument(
            "--json-output",
            type=str,
            nargs='?',
            choices=['pretty', 'default'],
            default='pretty',
            help="Provide the format of JSON output."
        )
        get_group_roles.add_argument(
            "--yaml-output",
            type=str,
            nargs='?',
            choices=['true', 'false'],
            default='false',
            help="Provide true to get output in YAML format."
        )

        list_group_roles = subparser.add_parser(
            'list-groups-roles',
            help='To list all the Groups Roles.',
            formatter_class=ArgumentDefaultsHelpFormatter)
        list_group_roles.add_argument(
            "--page_number",
            type=int,
            nargs=1,
            default=1,
            help="To list groups roles for a specific page_number."
        )
        list_group_roles.add_argument(
            "--limit",
            type=int,
            nargs=1,
            default=100,
            help="Provide limit to list number of groups roles."
        )
        list_group_roles.add_argument(
            "--json-output",
            type=str,
            nargs='?',
            choices=['pretty', 'default'],
            default='pretty',
            help="Provide the format of JSON output."
        )
        list_group_roles.add_argument(
            "--yaml-output",
            type=str,
            nargs='?',
            choices=['true', 'false'],
            default='false',
            help="Provide true to get output in YAML format."
        )

        get_role_groups = subparser.add_parser(
            'get-role-groups',
            help='To get all the groups in a specific Role.',
            formatter_class=ArgumentDefaultsHelpFormatter)
        get_role_groups.add_argument(
            "--role_id",
            type=int,
            nargs=1,
            default=SUPPRESS,
            required=True,
            help="Provide Role Id to get groups in a specific Role."
        )
        get_role_groups.add_argument(
            "--json-output",
            type=str,
            nargs='?',
            choices=['pretty', 'default'],
            default='pretty',
            help="Provide the format of JSON output."
        )
        get_role_groups.add_argument(
            "--yaml-output",
            type=str,
            nargs='?',
            choices=['true', 'false'],
            default='false',
            help="Provide true to get output in YAML format."
        )

        create_user_role = subparser.add_parser(
            'create-user-role',
            help='To create an User Role.',
            formatter_class=ArgumentDefaultsHelpFormatter)
        create_user_role.add_argument(
            "--user_id",
            type=int,
            nargs=1,
            default=SUPPRESS,
            required=True,
            help="Provide User Id to create-user-role."
        )
        create_user_role.add_argument(
            "--role_id",
            type=int,
            nargs=1,
            default=SUPPRESS,
            required=True,
            help="Provide Role Id to create-user-role."
        )
        create_user_role.add_argument(
            "--json-output",
            type=str,
            nargs='?',
            choices=['pretty', 'default'],
            default='pretty',
            help="Provide the format of JSON output."
        )
        create_user_role.add_argument(
            "--yaml-output",
            type=str,
            nargs='?',
            choices=['true', 'false'],
            default='false',
            help="Provide true to get output in YAML format."
        )

        delete_user_role = subparser.add_parser(
            'delete-user-role',
            help='To delete an User Role.',
            formatter_class=ArgumentDefaultsHelpFormatter)
        delete_user_role.add_argument(
            "--user_id",
            type=int,
            nargs=1,
            default=SUPPRESS,
            required=True,
            help="Provide User Id to delete-user-role."
        )
        delete_user_role.add_argument(
            "--role_id",
            type=int,
            nargs=1,
            default=SUPPRESS,
            required=True,
            help="Provide Role Id to delete-user-role."
        )
        delete_user_role.add_argument(
            "--json-output",
            type=str,
            nargs='?',
            choices=['pretty', 'default'],
            default='pretty',
            help="Provide the format of JSON output."
        )
        delete_user_role.add_argument(
            "--yaml-output",
            type=str,
            nargs='?',
            choices=['true', 'false'],
            default='false',
            help="Provide true to get output in YAML format."
        )

        create_group_role = subparser.add_parser(
            'create-group-role',
            help='To create a Group Role.',
            formatter_class=ArgumentDefaultsHelpFormatter)
        create_group_role.add_argument(
            "--group_id",
            type=int,
            nargs=1,
            default=SUPPRESS,
            required=True,
            help="Provide Group Id to create-group-role."
        )
        create_group_role.add_argument(
            "--role_id",
            type=int,
            nargs=1,
            default=SUPPRESS,
            required=True,
            help="Provide Role Id to create-group-role."
        )
        create_group_role.add_argument(
            "--json-output",
            type=str,
            nargs='?',
            choices=['pretty', 'default'],
            default='pretty',
            help="Provide the format of JSON output."
        )
        create_group_role.add_argument(
            "--yaml-output",
            type=str,
            nargs='?',
            choices=['true', 'false'],
            default='false',
            help="Provide true to get output in YAML format."
        )

        delete_group_role = subparser.add_parser(
            'delete-group-role',
            help='To delete a group Role.',
            formatter_class=ArgumentDefaultsHelpFormatter)
        delete_group_role.add_argument(
            "--group_id",
            type=int,
            nargs=1,
            default=SUPPRESS,
            required=True,
            help="Provide Group Id to delete-group-role."
        )
        delete_group_role.add_argument(
            "--role_id",
            type=int,
            nargs=1,
            default=SUPPRESS,
            required=True,
            help="Provide Role Id to delete-group-role."
        )
        delete_group_role.add_argument(
            "--json-output",
            type=str,
            nargs='?',
            choices=['pretty', 'default'],
            default='pretty',
            help="Provide the format of JSON output."
        )
        delete_group_role.add_argument(
            "--yaml-output",
            type=str,
            nargs='?',
            choices=['true', 'false'],
            default='false',
            help="Provide true to get output in YAML format."
        )

    def platform_admin_parser(subparser):
        list_tenant_users = subparser.add_parser(
            'list-tenant-users',
            help='To list all the users present in a tenant.',
            formatter_class=ArgumentDefaultsHelpFormatter)
        list_tenant_users.add_argument(
            "--tenant_id",
            type=str,
            nargs=1,
            required=True,
            default=SUPPRESS,
            help="Provide Tenant Id to list all the users present in it."
        )
        list_tenant_users.add_argument(
            "--page_number",
            type=int,
            nargs=1,
            default=1,
            help="To list tenant users for a specific page_number."
        )
        list_tenant_users.add_argument(
            "--limit",
            type=int,
            nargs=1,
            default=100,
            help="Provide limit to list number of tenant users."
        )
        list_tenant_users.add_argument(
            "--json-output",
            type=str,
            nargs='?',
            choices=['pretty', 'default'],
            default='pretty',
            help="Provide the format of JSON output."
        )
        list_tenant_users.add_argument(
            "--yaml-output",
            type=str,
            nargs='?',
            choices=['true', 'false'],
            default='false',
            help="Provide true to get output in YAML format."
        )

        get_tenant_user = subparser.add_parser(
            'get-tenant-user',
            help='To get information about a User present in a specific tenant.',
            formatter_class=ArgumentDefaultsHelpFormatter)
        get_tenant_user.add_argument(
            "--tenant_id",
            type=str,
            nargs=1,
            default=SUPPRESS,
            required=True,
            help="Provide Tenant Id to get information about a specific User."
        )
        get_tenant_user.add_argument(
            "--user_id",
            type=int,
            nargs=1,
            default=SUPPRESS,
            required=True,
            help="Provide User Id to get information about a specific User."
        )
        get_tenant_user.add_argument(
            "--json-output",
            type=str,
            nargs='?',
            choices=['pretty', 'default'],
            default='pretty',
            help="Provide the format of JSON output."
        )
        get_tenant_user.add_argument(
            "--yaml-output",
            type=str,
            nargs='?',
            choices=['true', 'false'],
            default='false',
            help="Provide true to get output in YAML format."
        )

        get_user_roles = subparser.add_parser(
            'get-user-roles',
            help='To get all the roles of an User present in a specific tenant.',
            formatter_class=ArgumentDefaultsHelpFormatter)
        get_user_roles.add_argument(
            "--tenant_id",
            type=str,
            nargs=1,
            default=SUPPRESS,
            required=True,
            help="Provide Tenant Id to get roles of a specific User."
        )
        get_user_roles.add_argument(
            "--user_id",
            type=int,
            nargs=1,
            default=SUPPRESS,
            required=True,
            help="Provide User Id to get roles of a specific User."
        )
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

        list_user_roles = subparser.add_parser(
            'list-users-roles',
            help='To list all the Users Roles in a specific tenant.',
            formatter_class=ArgumentDefaultsHelpFormatter)
        list_user_roles.add_argument(
            "--tenant_id",
            type=str,
            nargs=1,
            required=True,
            default=SUPPRESS,
            help="Provide Tenant Id to list User roles."
        )
        list_user_roles.add_argument(
            "--page_number",
            type=int,
            nargs=1,
            default=1,
            help="To list users roles for a specific page_number."
        )
        list_user_roles.add_argument(
            "--limit",
            type=int,
            nargs=1,
            default=100,
            help="Provide limit to list number of users roles."
        )
        list_user_roles.add_argument(
            "--json-output",
            type=str,
            nargs='?',
            choices=['pretty', 'default'],
            default='pretty',
            help="Provide the format of JSON output."
        )
        list_user_roles.add_argument(
            "--yaml-output",
            type=str,
            nargs='?',
            choices=['true', 'false'],
            default='false',
            help="Provide true to get output in YAML format."
        )

        get_role_users = subparser.add_parser(
            'get-role-users',
            help='To get all the users of a Role present in a specific tenant.',
            formatter_class=ArgumentDefaultsHelpFormatter)
        get_role_users.add_argument(
            "--tenant_id",
            type=str,
            nargs=1,
            default=SUPPRESS,
            required=True,
            help="Provide Tenant Id to get users in a specific Role."
        )
        get_role_users.add_argument(
            "--role_id",
            type=int,
            nargs=1,
            default=SUPPRESS,
            required=True,
            help="Provide Role Id to get users in a specific Role."
        )
        get_role_users.add_argument(
            "--json-output",
            type=str,
            nargs='?',
            choices=['pretty', 'default'],
            default='pretty',
            help="Provide the format of JSON output."
        )
        get_role_users.add_argument(
            "--yaml-output",
            type=str,
            nargs='?',
            choices=['true', 'false'],
            default='false',
            help="Provide true to get output in YAML format."
        )

        list_tenant_groups = subparser.add_parser(
            'list-tenant-groups',
            help='To list all the groups present in a tenant.',
            formatter_class=ArgumentDefaultsHelpFormatter)
        list_tenant_groups.add_argument(
            "--tenant_id",
            type=str,
            nargs=1,
            required=True,
            default=SUPPRESS,
            help="Provide Tenant Id to list all the groups present in it."
        )
        list_tenant_groups.add_argument(
            "--page_number",
            type=int,
            nargs=1,
            default=1,
            help="To list tenant groups for a specific page_number."
        )
        list_tenant_groups.add_argument(
            "--limit",
            type=int,
            nargs=1,
            default=100,
            help="Provide limit to list number of tenant groups."
        )
        list_tenant_groups.add_argument(
            "--json-output",
            type=str,
            nargs='?',
            choices=['pretty', 'default'],
            default='pretty',
            help="Provide the format of JSON output."
        )
        list_tenant_groups.add_argument(
            "--yaml-output",
            type=str,
            nargs='?',
            choices=['true', 'false'],
            default='false',
            help="Provide true to get output in YAML format."
        )

        get_tenant_group = subparser.add_parser(
            'get-tenant-group',
            help='To get information about a Group present in a specific tenant.',
            formatter_class=ArgumentDefaultsHelpFormatter)
        get_tenant_group.add_argument(
            "--tenant_id",
            type=str,
            nargs=1,
            default=SUPPRESS,
            required=True,
            help="Provide Tenant Id to get information about a specific Group."
        )
        get_tenant_group.add_argument(
            "--group_id",
            type=int,
            nargs=1,
            default=SUPPRESS,
            required=True,
            help="Provide Group Id to get information about a specific Group."
        )
        get_tenant_group.add_argument(
            "--json-output",
            type=str,
            nargs='?',
            choices=['pretty', 'default'],
            default='pretty',
            help="Provide the format of JSON output."
        )
        get_tenant_group.add_argument(
            "--yaml-output",
            type=str,
            nargs='?',
            choices=['true', 'false'],
            default='false',
            help="Provide true to get output in YAML format."
        )

        get_group_roles = subparser.add_parser(
            'get-group-roles',
            help='To get all the roles of a Group present in a specific tenant.',
            formatter_class=ArgumentDefaultsHelpFormatter)
        get_group_roles.add_argument(
            "--tenant_id",
            type=str,
            nargs=1,
            default=SUPPRESS,
            required=True,
            help="Provide Tenant Id to get roles of a specific Group."
        )
        get_group_roles.add_argument(
            "--group_id",
            type=int,
            nargs=1,
            default=SUPPRESS,
            required=True,
            help="Provide Group Id to get roles of a specific Group."
        )
        get_group_roles.add_argument(
            "--json-output",
            type=str,
            nargs='?',
            choices=['pretty', 'default'],
            default='pretty',
            help="Provide the format of JSON output."
        )
        get_group_roles.add_argument(
            "--yaml-output",
            type=str,
            nargs='?',
            choices=['true', 'false'],
            default='false',
            help="Provide true to get output in YAML format."
        )

        list_group_roles = subparser.add_parser(
            'list-groups-roles',
            help='To list all the Groups Roles in a specific tenant.',
            formatter_class=ArgumentDefaultsHelpFormatter)
        list_group_roles.add_argument(
            "--tenant_id",
            type=str,
            nargs=1,
            required=True,
            default=SUPPRESS,
            help="Provide Tenant Id to list Group roles."
        )
        list_group_roles.add_argument(
            "--page_number",
            type=int,
            nargs=1,
            default=1,
            help="To list groups roles for a specific page_number."
        )
        list_group_roles.add_argument(
            "--limit",
            type=int,
            nargs=1,
            default=100,
            help="Provide limit to list number of groups roles."
        )
        list_group_roles.add_argument(
            "--json-output",
            type=str,
            nargs='?',
            choices=['pretty', 'default'],
            default='pretty',
            help="Provide the format of JSON output."
        )
        list_group_roles.add_argument(
            "--yaml-output",
            type=str,
            nargs='?',
            choices=['true', 'false'],
            default='false',
            help="Provide true to get output in YAML format."
        )

        get_role_groups = subparser.add_parser(
            'get-role-groups',
            help='To get all the groups having a specific Role present in a specific tenant.',
            formatter_class=ArgumentDefaultsHelpFormatter)
        get_role_groups.add_argument(
            "--tenant_id",
            type=str,
            nargs=1,
            default=SUPPRESS,
            required=True,
            help="Provide Tenant Id to get groups in a specific Role."
        )
        get_role_groups.add_argument(
            "--role_id",
            type=int,
            nargs=1,
            default=SUPPRESS,
            required=True,
            help="Provide Role Id to get groups in a specific Role."
        )
        get_role_groups.add_argument(
            "--json-output",
            type=str,
            nargs='?',
            choices=['pretty', 'default'],
            default='pretty',
            help="Provide the format of JSON output."
        )
        get_role_groups.add_argument(
            "--yaml-output",
            type=str,
            nargs='?',
            choices=['true', 'false'],
            default='false',
            help="Provide true to get output in YAML format."
        )

        create_user_role = subparser.add_parser(
            'create-user-role',
            help='To create an User Role for a specific tenant.',
            formatter_class=ArgumentDefaultsHelpFormatter)
        create_user_role.add_argument(
            "--tenant_id",
            type=str,
            nargs=1,
            default=SUPPRESS,
            help="Provide Tenant Id to create-user-role."
        )
        create_user_role.add_argument(
            "--user_id",
            type=int,
            nargs=1,
            default=SUPPRESS,
            required=True,
            help="Provide User Id to create-user-role."
        )
        create_user_role.add_argument(
            "--role_id",
            type=int,
            nargs=1,
            default=SUPPRESS,
            required=True,
            help="Provide Role Id to create-user-role."
        )
        create_user_role.add_argument(
            "--json-output",
            type=str,
            nargs='?',
            choices=['pretty', 'default'],
            default='pretty',
            help="Provide the format of JSON output."
        )
        create_user_role.add_argument(
            "--yaml-output",
            type=str,
            nargs='?',
            choices=['true', 'false'],
            default='false',
            help="Provide true to get output in YAML format."
        )

        delete_user_role = subparser.add_parser(
            'delete-user-role',
            help='To delete an User Role of a specific tenant.',
            formatter_class=ArgumentDefaultsHelpFormatter)
        delete_user_role.add_argument(
            "--tenant_id",
            type=str,
            nargs=1,
            default=SUPPRESS,
            help="Provide Tenant Id to delete-user-role."
        )
        delete_user_role.add_argument(
            "--user_id",
            type=int,
            nargs=1,
            default=SUPPRESS,
            required=True,
            help="Provide User Id to delete-user-role."
        )
        delete_user_role.add_argument(
            "--role_id",
            type=int,
            nargs=1,
            default=SUPPRESS,
            required=True,
            help="Provide Role Id to delete-user-role."
        )
        delete_user_role.add_argument(
            "--json-output",
            type=str,
            nargs='?',
            choices=['pretty', 'default'],
            default='pretty',
            help="Provide the format of JSON output."
        )
        delete_user_role.add_argument(
            "--yaml-output",
            type=str,
            nargs='?',
            choices=['true', 'false'],
            default='false',
            help="Provide true to get output in YAML format."
        )

        create_group_role = subparser.add_parser(
            'create-group-role',
            help='To create a Group Role for a specific tenant.',
            formatter_class=ArgumentDefaultsHelpFormatter)
        create_group_role.add_argument(
            "--tenant_id",
            type=str,
            nargs=1,
            default=SUPPRESS,
            help="Provide Tenant Id to create-group-role."
        )
        create_group_role.add_argument(
            "--group_id",
            type=int,
            nargs=1,
            default=SUPPRESS,
            required=True,
            help="Provide Group Id to create-group-role."
        )
        create_group_role.add_argument(
            "--role_id",
            type=int,
            nargs=1,
            default=SUPPRESS,
            required=True,
            help="Provide Role Id to create-group-role."
        )
        create_group_role.add_argument(
            "--json-output",
            type=str,
            nargs='?',
            choices=['pretty', 'default'],
            default='pretty',
            help="Provide the format of JSON output."
        )
        create_group_role.add_argument(
            "--yaml-output",
            type=str,
            nargs='?',
            choices=['true', 'false'],
            default='false',
            help="Provide true to get output in YAML format."
        )

        delete_group_role = subparser.add_parser(
            'delete-group-role',
            help='To delete a Group Role of a specific tenant.',
            formatter_class=ArgumentDefaultsHelpFormatter)
        delete_group_role.add_argument(
            "--tenant_id",
            type=str,
            nargs=1,
            default=SUPPRESS,
            help="Provide Tenant Id to delete-group-role."
        )
        delete_group_role.add_argument(
            "--group_id",
            type=int,
            nargs=1,
            default=SUPPRESS,
            required=True,
            help="Provide Group Id to delete-group-role."
        )
        delete_group_role.add_argument(
            "--role_id",
            type=int,
            nargs=1,
            default=SUPPRESS,
            required=True,
            help="Provide Role Id to delete-group-role."
        )
        delete_group_role.add_argument(
            "--json-output",
            type=str,
            nargs='?',
            choices=['pretty', 'default'],
            default='pretty',
            help="Provide the format of JSON output."
        )
        delete_group_role.add_argument(
            "--yaml-output",
            type=str,
            nargs='?',
            choices=['true', 'false'],
            default='false',
            help="Provide true to get output in YAML format."
        )
