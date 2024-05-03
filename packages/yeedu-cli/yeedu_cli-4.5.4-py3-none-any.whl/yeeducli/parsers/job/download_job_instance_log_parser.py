from argparse import SUPPRESS, ArgumentDefaultsHelpFormatter


class DownloadJobInstanceLogParser:

    def download_job_instance_log_parser(subparser):

        download_Job_instance_logs = subparser.add_parser(
            'logs',
            help='To download Spark Job Instance logs for specific Spark Job Instance Id',
            formatter_class=ArgumentDefaultsHelpFormatter
        )
        download_Job_instance_logs.add_argument(
            "--job_id",
            type=int,
            nargs=1,
            default=SUPPRESS,
            required=True,
            help="Provide job_id to download log records."
        )
        download_Job_instance_logs.add_argument(
            "--log_type",
            type=str,
            nargs=1,
            default='stdout',
            choices=['stdout', 'stderr'],
            help="Provide log_type to download Spark Job Instance log records."
        )
        download_Job_instance_logs.add_argument(
            "--json-output",
            type=str,
            nargs='?',
            choices=['pretty', 'default'],
            default='pretty',
            help="Provide the format of JSON output."
        )
        download_Job_instance_logs.add_argument(
            "--yaml-output",
            type=str,
            nargs='?',
            choices=['true', 'false'],
            default='false',
            help="Provide true to get output in YAML format."
        )
