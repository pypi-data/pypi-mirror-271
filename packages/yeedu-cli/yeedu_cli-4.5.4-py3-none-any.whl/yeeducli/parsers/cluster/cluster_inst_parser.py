from argparse import SUPPRESS, ArgumentDefaultsHelpFormatter


class ClusterInstanceParser:

    def cluster_instance_parser(subparser):
        create_cluster_inst = subparser.add_parser(
            'create',
            help='To create the Cluster Instance.',
            formatter_class=ArgumentDefaultsHelpFormatter)
        create_cluster_inst.add_argument(
            "--instance_name",
            type=str,
            nargs='?',
            default=SUPPRESS,
            help="Provide instance_name to create."
        )
        create_cluster_inst.add_argument(
            "--idle_timeout_ms",
            type=int,
            nargs='?',
            default=SUPPRESS,
            required=True,
            help="Provide idle_timeout_ms to create."
        )
        create_cluster_inst.add_argument(
            "--auto_shutdown",
            type=str,
            nargs='?',
            default='true',
            metavar='true,false',
            help="Provide auto_shutdown to create."
        )
        create_cluster_inst.add_argument(
            "--cluster_conf_id",
            type=int,
            nargs=1,
            default=SUPPRESS,
            required=True,
            help="Provide cluster_conf_id to create."
        )
        create_cluster_inst.add_argument(
            "--json-output",
            type=str,
            nargs='?',
            choices=['pretty', 'default'],
            default='pretty',
            help="Provide the format of JSON output."
        )
        create_cluster_inst.add_argument(
            "--yaml-output",
            type=str,
            nargs='?',
            choices=['true', 'false'],
            default='false',
            help="Provide true to get output in YAML format."
        )

        list_cluster_inst = subparser.add_parser(
            'list',
            help='To list all the available Cluster Instances.',
            formatter_class=ArgumentDefaultsHelpFormatter)
        list_cluster_inst.add_argument(
            "--cluster_status",
            type=str,
            nargs="?",
            default=SUPPRESS,
            help='Provide Cluster Instance Status from ["INITIATING", "RUNNING", "STOPPING", "STOPPED", "DESTROYING", "DESTROYED", "ERROR", "RESIZING_UP", "RESIZING_DOWN"] to list, For example --cluster_status="RUNNING,DESTROYED".'
        )
        list_cluster_inst.add_argument(
            "--cluster_conf_id",
            type=int,
            nargs=1,
            default=SUPPRESS,
            help="Provide Cluster Conf Id to list all the Cluster Instances."
        )
        list_cluster_inst.add_argument(
            "--cluster_conf_name",
            type=str,
            nargs=1,
            default=SUPPRESS,
            help="Provide Engine Cluster Config Name to list all the Cluster Instances."
        )
        list_cluster_inst.add_argument(
            "--page_number",
            # type=check_minimum,
            type=int,
            nargs=1,
            default=1,
            help="To list Cluster Instance for a specific page_number."
        )
        list_cluster_inst.add_argument(
            "--limit",
            # type=check_range(1, 1000),
            type=int,
            nargs=1,
            default=100,
            help="Provide limit to list number of Cluster Instance."
        )
        list_cluster_inst.add_argument(
            "--json-output",
            type=str,
            nargs='?',
            choices=['pretty', 'default'],
            default='pretty',
            help="Provide the format of JSON output."
        )
        list_cluster_inst.add_argument(
            "--yaml-output",
            type=str,
            nargs='?',
            choices=['true', 'false'],
            default='false',
            help="Provide true to get output in YAML format."
        )

        get_cluster_inst = subparser.add_parser(
            'get',
            help='To get the information about a specific Cluster Instance.',
            formatter_class=ArgumentDefaultsHelpFormatter)
        get_cluster_inst.add_argument(
            "--cluster_id",
            type=int,
            nargs=1,
            default=SUPPRESS,
            help="Provide Cluster Instance Id to get information about a specific Cluster Instance."
        )
        get_cluster_inst.add_argument(
            "--cluster_name",
            type=str,
            nargs=1,
            default=SUPPRESS,
            help="Provide Cluster Instance Name to get information about a specific Cluster Instance."
        )
        get_cluster_inst.add_argument(
            "--json-output",
            type=str,
            nargs='?',
            choices=['pretty', 'default'],
            default='pretty',
            help="Provide the format of JSON output."
        )
        get_cluster_inst.add_argument(
            "--yaml-output",
            type=str,
            nargs='?',
            choices=['true', 'false'],
            default='false',
            help="Provide true to get output in YAML format."
        )

        edit_cluster_inst = subparser.add_parser(
            'edit',
            help='To edit a specific Cluster Instance.',
            formatter_class=ArgumentDefaultsHelpFormatter)
        edit_cluster_inst.add_argument(
            "--cluster_id",
            type=int,
            nargs=1,
            default=SUPPRESS,
            help="Provide a specific Cluster Instance Id to edit."
        )
        edit_cluster_inst.add_argument(
            "--cluster_name",
            type=str,
            nargs=1,
            default=SUPPRESS,
            help="Provide a specific Cluster Instance Name to edit."
        )
        edit_cluster_inst.add_argument(
            "--idle_timeout_ms",
            type=int,
            nargs='?',
            default=SUPPRESS,
            help="Provide idle_timeout_ms to edit."
        )
        edit_cluster_inst.add_argument(
            "--auto_shutdown",
            type=str,
            nargs='?',
            default=SUPPRESS,
            metavar='true,false',
            help="Provide auto_shutdown to edit."
        )
        edit_cluster_inst.add_argument(
            "--json-output",
            type=str,
            nargs='?',
            choices=['pretty', 'default'],
            default='pretty',
            help="Provide the format of JSON output."
        )
        edit_cluster_inst.add_argument(
            "--yaml-output",
            type=str,
            nargs='?',
            choices=['true', 'false'],
            default='false',
            help="Provide true to get output in YAML format."
        )

        start_cluster_inst = subparser.add_parser(
            'start',
            help='To start a specific Cluster Instance.',
            formatter_class=ArgumentDefaultsHelpFormatter)
        start_cluster_inst.add_argument(
            "--cluster_id",
            type=int,
            nargs=1,
            default=SUPPRESS,
            help="Provide Cluster Instance Id to start an Cluster Instance."
        )
        start_cluster_inst.add_argument(
            "--cluster_name",
            type=str,
            nargs=1,
            default=SUPPRESS,
            help="Provide Cluster Instance Name to start an Cluster Instance."
        )
        start_cluster_inst.add_argument(
            "--json-output",
            type=str,
            nargs='?',
            choices=['pretty', 'default'],
            default='pretty',
            help="Provide the format of JSON output."
        )
        start_cluster_inst.add_argument(
            "--yaml-output",
            type=str,
            nargs='?',
            choices=['true', 'false'],
            default='false',
            help="Provide true to get output in YAML format."
        )

        stop_cluster_inst = subparser.add_parser(
            'stop',
            help='To stop a specific Cluster Instance.',
            formatter_class=ArgumentDefaultsHelpFormatter)
        stop_cluster_inst.add_argument(
            "--cluster_id",
            type=int,
            nargs=1,
            default=SUPPRESS,
            help="Provide Cluster Instance Id to stop an Cluster Instance."
        )
        stop_cluster_inst.add_argument(
            "--cluster_name",
            type=str,
            nargs=1,
            default=SUPPRESS,
            help="Provide Cluster Instance Name to stop an Cluster Instance."
        )
        stop_cluster_inst.add_argument(
            "--json-output",
            type=str,
            nargs='?',
            choices=['pretty', 'default'],
            default='pretty',
            help="Provide the format of JSON output."
        )
        stop_cluster_inst.add_argument(
            "--yaml-output",
            type=str,
            nargs='?',
            choices=['true', 'false'],
            default='false',
            help="Provide true to get output in YAML format."
        )

        destroy_cluster_inst = subparser.add_parser(
            'destroy',
            help='To destroy a specific Cluster Instance.',
            formatter_class=ArgumentDefaultsHelpFormatter)
        destroy_cluster_inst.add_argument(
            "--cluster_id",
            type=int,
            nargs=1,
            default=SUPPRESS,
            help="Provide Cluster Instance Id to destroy an Cluster Instance."
        )
        destroy_cluster_inst.add_argument(
            "--cluster_name",
            type=str,
            nargs=1,
            default=SUPPRESS,
            help="Provide Cluster Instance Name to destroy an Cluster Instance."
        )
        destroy_cluster_inst.add_argument(
            "--json-output",
            type=str,
            nargs='?',
            choices=['pretty', 'default'],
            default='pretty',
            help="Provide the format of JSON output."
        )
        destroy_cluster_inst.add_argument(
            "--yaml-output",
            type=str,
            nargs='?',
            choices=['true', 'false'],
            default='false',
            help="Provide true to get output in YAML format."
        )

        uptime_cluster_inst = subparser.add_parser(
            'uptime',
            help='To get total uptime of a specific Cluster Instance.',
            formatter_class=ArgumentDefaultsHelpFormatter)
        uptime_cluster_inst.add_argument(
            "--cluster_id",
            type=int,
            nargs=1,
            default=SUPPRESS,
            help="Provide Cluster Instance Id to get toatl uptime of an Cluster Instance."
        )
        uptime_cluster_inst.add_argument(
            "--cluster_name",
            type=str,
            nargs=1,
            default=SUPPRESS,
            help="Provide Cluster Instance Name to destroy an Cluster Instance."
        )
        uptime_cluster_inst.add_argument(
            "--json-output",
            type=str,
            nargs='?',
            choices=['pretty', 'default'],
            default='pretty',
            help="Provide the format of JSON output."
        )
        uptime_cluster_inst.add_argument(
            "--yaml-output",
            type=str,
            nargs='?',
            choices=['true', 'false'],
            default='false',
            help="Provide true to get output in YAML format."
        )

        get_job_stats_by_cluster_inst = subparser.add_parser(
            'get-stats',
            help='To get the Spark Job Statistics of an Cluster Instance.',
            formatter_class=ArgumentDefaultsHelpFormatter)
        get_job_stats_by_cluster_inst.add_argument(
            "--cluster_id",
            type=int,
            nargs=1,
            default=SUPPRESS,
            help="Provide Cluster Instance Id to get the Spark Job Statistics of an Cluster Instance."
        )
        get_job_stats_by_cluster_inst.add_argument(
            "--cluster_name",
            type=str,
            nargs=1,
            default=SUPPRESS,
            help="Provide Cluster Instance Name to get the Spark Job Statistics of an Cluster Instance."
        )
        get_job_stats_by_cluster_inst.add_argument(
            "--json-output",
            type=str,
            nargs='?',
            choices=['pretty', 'default'],
            default='pretty',
            help="Provide the format of JSON output."
        )
        get_job_stats_by_cluster_inst.add_argument(
            "--yaml-output",
            type=str,
            nargs='?',
            choices=['true', 'false'],
            default='false',
            help="Provide true to get output in YAML format."
        )
