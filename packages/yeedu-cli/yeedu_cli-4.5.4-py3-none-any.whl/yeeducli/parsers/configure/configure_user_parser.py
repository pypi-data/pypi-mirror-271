from argparse import SUPPRESS


class ConfigureUserParser:

    def configure_user_parser(configure_user_parser):
        configure_user_parser.add_argument(
            "--timeout",
            type=str,
            nargs='?',
            default="48",
            help="Provide token expiration timeout in hour Example: --timeout=24,--timeout=infinity (infinity for no expiration time) to generate Yeedu Token."
        )
        configure_user_parser.add_argument(
            "--json-output",
            type=str,
            nargs='?',
            choices=['pretty', 'default'],
            default='pretty',
            help="Provide the format of JSON output."
        )
        configure_user_parser.add_argument(
            "--yaml-output",
            type=str,
            nargs='?',
            choices=['true', 'false'],
            default='false',
            help="Provide true to get output in YAML format."
        )

    def user_logout_parser(user_logout_parser):
        user_logout_parser.add_argument(
            "--json-output",
            type=str,
            nargs='?',
            choices=['pretty', 'default'],
            default='pretty',
            help="Provide the format of JSON output."
        )
        user_logout_parser.add_argument(
            "--yaml-output",
            type=str,
            nargs='?',
            choices=['true', 'false'],
            default='false',
            help="Provide true to get output in YAML format."
        )
