from yeeducli.constants import SPARK_DEPLOYMENT_MODE_LIST
from argparse import SUPPRESS, ArgumentDefaultsHelpFormatter


class SparkJobConfigurationParser:

    def spark_job_configuration_parser(subparser):

        create_spark_job_conf = subparser.add_parser(
            'create-conf',
            help='To create a Spark Job Configuration.',
            formatter_class=ArgumentDefaultsHelpFormatter)
        create_spark_job_conf.add_argument(
            "--cluster_id",
            type=int,
            nargs=1,
            default=SUPPRESS,
            required=True,
            help="Provide cluster_id to create a Spark Job Configuration."
        )
        create_spark_job_conf.add_argument(
            "--name",
            type=str,
            nargs=1,
            default=SUPPRESS,
            required=True,
            help="Provide name to create a Spark Job Configuration."
        )
        create_spark_job_conf.add_argument(
            "--files",
            type=str,
            nargs='?',
            default=SUPPRESS,
            help="Provide files to create a Spark Job Configuration."
        )
        create_spark_job_conf.add_argument(
            "--properties-file",
            type=str,
            nargs='?',
            default=SUPPRESS,
            help="Provide properties-file to create a Spark Job Configuration."
        )
        create_spark_job_conf.add_argument(
            "--conf",
            type=str,
            action='append',
            nargs='+',
            default=SUPPRESS,
            help="Provide conf to create a Spark Job Configuration."
        )
        create_spark_job_conf.add_argument(
            "--packages",
            type=str,
            nargs='?',
            default=SUPPRESS,
            help="Provide packages to create a Spark Job Configuration."
        )
        create_spark_job_conf.add_argument(
            "--repositories",
            type=str,
            nargs='?',
            default=SUPPRESS,
            help="Provide repositories to create a Spark Job Configuration."
        )
        create_spark_job_conf.add_argument(
            "--jars",
            type=str,
            nargs='?',
            default=SUPPRESS,
            help="Provide jars to create a Spark Job Configuration."
        )
        create_spark_job_conf.add_argument(
            "--archives",
            type=str,
            nargs='?',
            default=SUPPRESS,
            help="Provide archives to create a Spark Job Configuration."
        )
        create_spark_job_conf.add_argument(
            "--deploy-mode",
            type=str,
            nargs=1,
            default=SUPPRESS,
            required=True,
            metavar='client,cluster',
            choices=SPARK_DEPLOYMENT_MODE_LIST,
            help="Provide deploy-mode to create a Spark Job Configuration."
        )
        create_spark_job_conf.add_argument(
            "--driver-memory",
            type=str,
            nargs='?',
            default=SUPPRESS,
            help="Provide driver-memory to create a Spark Job Configuration."
        )
        create_spark_job_conf.add_argument(
            "--driver-java-options",
            type=str,
            nargs='?',
            default=SUPPRESS,
            help="Provide driver-java-options to create a Spark Job Configuration."
        )
        create_spark_job_conf.add_argument(
            "--driver-library-path",
            type=str,
            nargs='?',
            default=SUPPRESS,
            help="Provide driver-library-path to create a Spark Job Configuration."
        )
        create_spark_job_conf.add_argument(
            "--driver-class-path",
            type=str,
            nargs='?',
            default=SUPPRESS,
            help="Provide driver-class-path to create a Spark Job Configuration."
        )
        create_spark_job_conf.add_argument(
            "--executor-memory",
            type=str,
            nargs='?',
            default=SUPPRESS,
            help="Provide executor-memory to create a Spark Job Configuration."
        )
        create_spark_job_conf.add_argument(
            "--driver-cores",
            type=int,
            nargs='?',
            default=SUPPRESS,
            help="Provide driver-cores to create a Spark Job Configuration."
        )
        create_spark_job_conf.add_argument(
            "--total-executor-cores",
            type=int,
            nargs='?',
            default=SUPPRESS,
            help="Provide total-executor-cores to create a Spark Job Configuration."
        )
        create_spark_job_conf.add_argument(
            "--executor-cores",
            type=int,
            nargs='?',
            default=SUPPRESS,
            help="Provide executor-cores to create a Spark Job Configuration."
        )
        create_spark_job_conf.add_argument(
            "--num-executors",
            type=int,
            nargs='?',
            default=SUPPRESS,
            help="Provide num-executors to create a Spark Job Configuration."
        )
        create_spark_job_conf.add_argument(
            "--principal",
            type=str,
            nargs='?',
            default=SUPPRESS,
            help="Provide principal to create a Spark Job Configuration."
        )
        create_spark_job_conf.add_argument(
            "--keytab",
            type=str,
            nargs='?',
            default=SUPPRESS,
            help="Provide keytab to create a Spark Job Configuration."
        )
        create_spark_job_conf.add_argument(
            "--queue",
            type=str,
            nargs='?',
            default=SUPPRESS,
            help="Provide queue to create a Spark Job Configuration."
        )
        create_spark_job_conf.add_argument(
            "--class-name",
            type=str,
            nargs='?',
            default=SUPPRESS,
            help="Provide class-name to create a Spark Job Configuration."
        )
        create_spark_job_conf.add_argument(
            "--command",
            type=str,
            nargs='?',
            default=SUPPRESS,
            help="Provide command to create a Spark Job Configuration."
        )
        create_spark_job_conf.add_argument(
            "--arguments",
            type=str,
            nargs='?',
            default=SUPPRESS,
            help="Provide arguments to create a Spark Job Configuration."
        )
        create_spark_job_conf.add_argument(
            "--raw-scala-code",
            type=str,
            nargs=1,
            default=SUPPRESS,
            help="Provide raw-scala-code file path to create a Spark Job Configuration."
        )
        create_spark_job_conf.add_argument(
            "--max_concurrency",
            type=int,
            nargs=1,
            default=SUPPRESS,
            help="Provide max_concurrency number to limit the number of jobs submitted."
        )
        create_spark_job_conf.add_argument(
            "--json-output",
            type=str,
            nargs='?',
            choices=['pretty', 'default'],
            default='pretty',
            help="Provide the format of JSON output."
        )
        create_spark_job_conf.add_argument(
            "--yaml-output",
            type=str,
            nargs='?',
            choices=['true', 'false'],
            default='false',
            help="Provide true to get output in YAML format."
        )

        list_spark_job_conf = subparser.add_parser(
            'list-confs',
            help='To list all the available Spark Job Configurations.',
            formatter_class=ArgumentDefaultsHelpFormatter)
        list_spark_job_conf.add_argument(
            "--page_number",
            # type=check_minimum,
            type=int,
            nargs=1,
            default=1,
            help="To list Spark Job Configurations for a specific page_number."
        )
        list_spark_job_conf.add_argument(
            "--limit",
            # type=check_range(1, 1000),
            type=int,
            nargs=1,
            default=100,
            help="Provide limit to list number of Spark Job Configurations."
        )
        list_spark_job_conf.add_argument(
            "--json-output",
            type=str,
            nargs='?',
            choices=['pretty', 'default'],
            default='pretty',
            help="Provide the format of JSON output."
        )
        list_spark_job_conf.add_argument(
            "--yaml-output",
            type=str,
            nargs='?',
            choices=['true', 'false'],
            default='false',
            help="Provide true to get output in YAML format."
        )

        describe_spark_job_conf = subparser.add_parser(
            'get-conf',
            help='To get information about a specific Spark Job Configuration.',
            formatter_class=ArgumentDefaultsHelpFormatter)
        describe_spark_job_conf.add_argument(
            "--job_conf_id",
            type=int,
            nargs=1,
            default=SUPPRESS,
            help="Provide an id to get information about a specific Spark Job Configuration."
        )
        describe_spark_job_conf.add_argument(
            "--job_conf_name",
            type=str,
            nargs=1,
            default=SUPPRESS,
            help="Provide name to get information about a specific Spark Job Configuration."
        )
        describe_spark_job_conf.add_argument(
            "--json-output",
            type=str,
            nargs='?',
            choices=['pretty', 'default'],
            default='pretty',
            help="Provide the format of JSON output."
        )
        describe_spark_job_conf.add_argument(
            "--yaml-output",
            type=str,
            nargs='?',
            choices=['true', 'false'],
            default='false',
            help="Provide true to get output in YAML format."
        )

        edit_spark_job_conf = subparser.add_parser(
            'edit-conf',
            help='To edit a Spark Job Configuration.',
            formatter_class=ArgumentDefaultsHelpFormatter)
        edit_spark_job_conf.add_argument(
            "--job_conf_id",
            type=int,
            nargs=1,
            default=SUPPRESS,
            help="Provide Spark Job Config Id to edit a Spark Job Configuration."
        )
        edit_spark_job_conf.add_argument(
            "--job_conf_name",
            type=str,
            nargs=1,
            default=SUPPRESS,
            help="Provide Spark Job Config Name to edit a Spark Job Configuration."
        )
        edit_spark_job_conf.add_argument(
            "--cluster_id",
            type=int,
            nargs=1,
            default=SUPPRESS,
            help="Provide Cluster Id to edit in a Spark Job Configuration."
        )
        edit_spark_job_conf.add_argument(
            "--cluster_name",
            type=str,
            nargs=1,
            default=SUPPRESS,
            help="Provide Cluster Name to edit in a Spark Job Configuration."
        )
        edit_spark_job_conf.add_argument(
            "--files",
            type=str,
            nargs='?',
            default=SUPPRESS,
            help="Provide files to edit in a Spark Job Configuration."
        )
        edit_spark_job_conf.add_argument(
            "--properties-file",
            type=str,
            nargs='?',
            default=SUPPRESS,
            help="Provide properties-file to edit in a Spark Job Configuration."
        )
        edit_spark_job_conf.add_argument(
            "--conf",
            type=str,
            action='append',
            nargs='+',
            default=SUPPRESS,
            help="Provide conf to edit in a Spark Job Configuration."
        )
        edit_spark_job_conf.add_argument(
            "--packages",
            type=str,
            nargs='?',
            default=SUPPRESS,
            help="Provide packages to edit in a Spark Job Configuration."
        )
        edit_spark_job_conf.add_argument(
            "--repositories",
            type=str,
            nargs='?',
            default=SUPPRESS,
            help="Provide repositories to edit in a Spark Job Configuration."
        )
        edit_spark_job_conf.add_argument(
            "--jars",
            type=str,
            nargs='?',
            default=SUPPRESS,
            help="Provide jars to edit in a Spark Job Configuration."
        )
        edit_spark_job_conf.add_argument(
            "--archives",
            type=str,
            nargs='?',
            default=SUPPRESS,
            help="Provide archives to edit in a Spark Job Configuration."
        )
        edit_spark_job_conf.add_argument(
            "--deploy-mode",
            type=str,
            nargs=1,
            default=SUPPRESS,
            metavar='client,cluster',
            choices=SPARK_DEPLOYMENT_MODE_LIST,
            help="Provide deploy-mode to edit in a Spark Job Configuration."
        )
        edit_spark_job_conf.add_argument(
            "--driver-memory",
            type=str,
            nargs='?',
            default=SUPPRESS,
            help="Provide driver-memory to edit in a Spark Job Configuration."
        )
        edit_spark_job_conf.add_argument(
            "--driver-java-options",
            type=str,
            nargs='?',
            default=SUPPRESS,
            help="Provide driver-java-options to edit in a Spark Job Configuration."
        )
        edit_spark_job_conf.add_argument(
            "--driver-library-path",
            type=str,
            nargs='?',
            default=SUPPRESS,
            help="Provide driver-library-path to edit in a Spark Job Configuration."
        )
        edit_spark_job_conf.add_argument(
            "--driver-class-path",
            type=str,
            nargs='?',
            default=SUPPRESS,
            help="Provide driver-class-path to edit in a Spark Job Configuration."
        )
        edit_spark_job_conf.add_argument(
            "--executor-memory",
            type=str,
            nargs='?',
            default=SUPPRESS,
            help="Provide executor-memory to edit in a Spark Job Configuration."
        )
        edit_spark_job_conf.add_argument(
            "--driver-cores",
            type=int,
            nargs='?',
            default=SUPPRESS,
            help="Provide driver-cores to edit in a Spark Job Configuration."
        )
        edit_spark_job_conf.add_argument(
            "--total-executor-cores",
            type=int,
            nargs='?',
            default=SUPPRESS,
            help="Provide total-executor-cores to edit in a Spark Job Configuration."
        )
        edit_spark_job_conf.add_argument(
            "--executor-cores",
            type=int,
            nargs='?',
            default=SUPPRESS,
            help="Provide executor-cores to edit in a Spark Job Configuration."
        )
        edit_spark_job_conf.add_argument(
            "--num-executors",
            type=int,
            nargs='?',
            default=SUPPRESS,
            help="Provide num-executors to edit in a Spark Job Configuration."
        )
        edit_spark_job_conf.add_argument(
            "--principal",
            type=str,
            nargs='?',
            default=SUPPRESS,
            help="Provide principal to edit in a Spark Job Configuration."
        )
        edit_spark_job_conf.add_argument(
            "--keytab",
            type=str,
            nargs='?',
            default=SUPPRESS,
            help="Provide keytab to edit in a Spark Job Configuration."
        )
        edit_spark_job_conf.add_argument(
            "--queue",
            type=str,
            nargs='?',
            default=SUPPRESS,
            help="Provide queue to edit in a Spark Job Configuration."
        )
        edit_spark_job_conf.add_argument(
            "--class-name",
            type=str,
            nargs='?',
            default=SUPPRESS,
            help="Provide class-name to edit in a Spark Job Configuration."
        )
        edit_spark_job_conf.add_argument(
            "--name",
            type=str,
            nargs='?',
            default=SUPPRESS,
            help="Provide name to edit in a Spark Job Configuration."
        )
        edit_spark_job_conf.add_argument(
            "--command",
            type=str,
            nargs='?',
            default=SUPPRESS,
            help="Provide command to edit in a Spark Job Configuration."
        )
        edit_spark_job_conf.add_argument(
            "--arguments",
            type=str,
            nargs='?',
            default=SUPPRESS,
            help="Provide arguments to edit in a Spark Job Configuration."
        )
        edit_spark_job_conf.add_argument(
            "--raw-scala-code",
            type=str,
            nargs=1,
            default=SUPPRESS,
            help="Provide raw-scala-code file path to edit in a Spark Job Configuration."
        )
        edit_spark_job_conf.add_argument(
            "--max_concurrency",
            type=int,
            nargs=1,
            default=SUPPRESS,
            help="Provide max_concurrency number to limit the number of jobs submitted."
        )
        edit_spark_job_conf.add_argument(
            "--json-output",
            type=str,
            nargs='?',
            choices=['pretty', 'default'],
            default='pretty',
            help="Provide the format of JSON output."
        )
        edit_spark_job_conf.add_argument(
            "--yaml-output",
            type=str,
            nargs='?',
            choices=['true', 'false'],
            default='false',
            help="Provide true to get output in YAML format."
        )

        delete_spark_job_conf = subparser.add_parser(
            'delete-conf',
            help='To delete a specific Spark Job Configuration.',
            formatter_class=ArgumentDefaultsHelpFormatter)
        delete_spark_job_conf.add_argument(
            "--job_conf_id",
            type=int,
            nargs=1,
            default=SUPPRESS,
            help="Provide Job Conf Id to delete a Spark Job Configuration."
        )
        delete_spark_job_conf.add_argument(
            "--job_conf_name",
            type=str,
            nargs=1,
            default=SUPPRESS,
            help="Provide Job Conf Name to delete a Spark Job Configuration."
        )
        delete_spark_job_conf.add_argument(
            "--json-output",
            type=str,
            nargs='?',
            choices=['pretty', 'default'],
            default='pretty',
            help="Provide the format of JSON output."
        )
        delete_spark_job_conf.add_argument(
            "--yaml-output",
            type=str,
            nargs='?',
            choices=['true', 'false'],
            default='false',
            help="Provide true to get output in YAML format."
        )
