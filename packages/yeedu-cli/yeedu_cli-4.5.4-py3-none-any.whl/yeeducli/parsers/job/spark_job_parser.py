from yeeducli.constants import SPARK_JOB_STATUS
from argparse import SUPPRESS, ArgumentDefaultsHelpFormatter


class SparkJobInstanceParser:
    def spark_job_parser(subparser):
        start_spark_job_run = subparser.add_parser(
            'start',
            help='To run an Apache Spark job.',
            formatter_class=ArgumentDefaultsHelpFormatter)
        start_spark_job_run.add_argument(
            "--job_conf_id",
            type=int,
            nargs=1,
            default=SUPPRESS,
            help="To run an Apache Spark Job, enter job_conf_id."
        )
        start_spark_job_run.add_argument(
            "--job_conf_name",
            type=str,
            nargs=1,
            default=SUPPRESS,
            help="To run an Apache Spark Job, enter job_conf_name."
        )
        start_spark_job_run.add_argument(
            "--json-output",
            type=str,
            nargs='?',
            choices=['pretty', 'default'],
            default='pretty',
            help="Provide the format of JSON output."
        )
        start_spark_job_run.add_argument(
            "--yaml-output",
            type=str,
            nargs='?',
            choices=['true', 'false'],
            default='false',
            help="Provide true to get output in YAML format."
        )

        list_spark_job_inst = subparser.add_parser(
            'list',
            help='To list all the available Apache Spark Job Instances.',
            formatter_class=ArgumentDefaultsHelpFormatter)
        list_spark_job_inst.add_argument(
            "--cluster_id",
            type=int,
            nargs=1,
            default=SUPPRESS,
            required=True,
            help="To list Apache Spark Job of a specific cluster_id."
        )
        list_spark_job_inst.add_argument(
            "--job_conf_id",
            type=int,
            nargs=1,
            default=SUPPRESS,
            help="To list Apache Spark Job of a specific job_conf_id."
        )
        list_spark_job_inst.add_argument(
            "--job_conf_name",
            type=str,
            nargs=1,
            default=SUPPRESS,
            help="To list Apache Spark Job of a specific job_conf_name."
        )
        list_spark_job_inst.add_argument(
            "--job_status",
            type=str,
            nargs=1,
            default=SUPPRESS,
            choices=SPARK_JOB_STATUS,
            help="To list Apache Spark Job for a specific Spark job Status."
        )
        list_spark_job_inst.add_argument(
            "--page_number",
            # type=check_minimum,
            type=int,
            nargs=1,
            default=1,
            help="To list Apache Spark Job for a specific page_number."
        )
        list_spark_job_inst.add_argument(
            "--limit",
            # type=check_range(1, 1000),
            type=int,
            nargs=1,
            default=100,
            help="Provide limit to list number of Apache Spark Job Instance."
        )
        list_spark_job_inst.add_argument(
            "--json-output",
            type=str,
            nargs='?',
            choices=['pretty', 'default'],
            default='pretty',
            help="Provide the format of JSON output."
        )
        list_spark_job_inst.add_argument(
            "--yaml-output",
            type=str,
            nargs='?',
            choices=['true', 'false'],
            default='false',
            help="Provide true to get output in YAML format."
        )

        describe_spark_job_inst = subparser.add_parser(
            'get',
            help='To get information about a specific Apache Spark Job Instance.',
            formatter_class=ArgumentDefaultsHelpFormatter)
        describe_spark_job_inst.add_argument(
            "--job_id",
            type=int,
            nargs=1,
            default=SUPPRESS,
            required=True,
            help="Provide an job_id to get information about a specific Apache Spark Job Instance."
        )
        describe_spark_job_inst.add_argument(
            "--json-output",
            type=str,
            nargs='?',
            choices=['pretty', 'default'],
            default='pretty',
            help="Provide the format of JSON output."
        )
        describe_spark_job_inst.add_argument(
            "--yaml-output",
            type=str,
            nargs='?',
            choices=['true', 'false'],
            default='false',
            help="Provide true to get output in YAML format."
        )

        kill_spark_job_inst = subparser.add_parser(
            'kill',
            help='To kill a specific Apache Spark Job Instance.',
            formatter_class=ArgumentDefaultsHelpFormatter)
        kill_spark_job_inst.add_argument(
            "--job_id",
            type=int,
            nargs=1,
            default=SUPPRESS,
            required=True,
            help="Provide an job_id to kill a specific Apache Spark Job Instance."
        )
        kill_spark_job_inst.add_argument(
            "--json-output",
            type=str,
            nargs='?',
            choices=['pretty', 'default'],
            default='pretty',
            help="Provide the format of JSON output."
        )
        kill_spark_job_inst.add_argument(
            "--yaml-output",
            type=str,
            nargs='?',
            choices=['true', 'false'],
            default='false',
            help="Provide true to get output in YAML format."
        )

        get_workflow_job_inst = subparser.add_parser(
            'get-workflow-job-instance',
            help='To get information about a specific Workflow Job Instance.',
            formatter_class=ArgumentDefaultsHelpFormatter)
        get_workflow_job_inst.add_argument(
            "--job_application_id",
            type=str,
            nargs=1,
            default=SUPPRESS,
            required=True,
            help="Provide a job_application_id to get information about a specific Workflow Job Instance."
        )
        get_workflow_job_inst.add_argument(
            "--json-output",
            type=str,
            nargs='?',
            choices=['pretty', 'default'],
            default='pretty',
            help="Provide the format of JSON output."
        )
        get_workflow_job_inst.add_argument(
            "--yaml-output",
            type=str,
            nargs='?',
            choices=['true', 'false'],
            default='false',
            help="Provide true to get output in YAML format."
        )
