#!/usr/bin/env python3

from yeeducli.parsers.configure.configure_user_parser import ConfigureUserParser
from yeeducli.subcommand_module.service_subcommand import ServiceSubcommand
from yeeducli.parsers.service_parser import ServiceParser
from yeeducli.utility.logger_utils import Logger
from yeeducli.utility.json_utils import *
from argparse import ArgumentParser, SUPPRESS, ArgumentDefaultsHelpFormatter
from yeeducli.constants import *
import sys

logger = Logger.get_logger(__name__, True)


def yeedu():

    try:
        if len(sys.argv) > 1:
            if sys.argv[1] == 'resource':
                try:
                    if (sys.argv[2] in RESOURCE_LIST) or (sys.argv[2] in ['-h', '--help']):
                        # RESOURCE
                        parser, subparser = main_parser(sys.argv[1])
                        ServiceParser.create_service_parser(
                            sys.argv[1], subparser)
                        call_service_subcommand(parser)
                    else:
                        logger.error(
                            f"Please provide \"yeedu resource [resource-service]\"\n")
                        logger.error(get_similar_subcommand(
                            sys.argv[2], RESOURCE_LIST))
                        sys.exit(-1)
                except IndexError as e:
                    logger.error(
                        f"Please provide \"yeedu resource [-h] [resource-services]\"\n")
                    sys.exit(-1)

            elif sys.argv[1] == 'cluster':
                try:
                    if (sys.argv[2] in CLUSTER_LIST) or (sys.argv[2] in ['-h', '--help']):
                        # CLUSTER
                        parser, subparser = main_parser(sys.argv[1])
                        ServiceParser.create_service_parser(
                            sys.argv[1], subparser)
                        call_service_subcommand(parser, sys.argv[1])
                    else:
                        logger.error(
                            f"Please provide \"yeedu cluster [cluster-service]\"\n")
                        logger.error(get_similar_subcommand(
                            sys.argv[2], CLUSTER_LIST))
                        sys.exit(-1)
                except IndexError as e:
                    logger.error(
                        f"Please provide \"yeedu cluster [-h] [cluster-services]\"\n")
                    sys.exit(-1)

            elif sys.argv[1] == 'job':
                try:
                    if sys.argv[2] in JOB_LIST or sys.argv[2] in ['-h', '--help']:
                        # USI
                        parser, subparser = main_parser(sys.argv[1])
                        ServiceParser.create_service_parser(
                            sys.argv[1], subparser)
                        call_service_subcommand(parser, sys.argv[1])
                    else:
                        logger.error(
                            f"Please provide \"yeedu job [job-service]\"\n")
                        logger.error(get_similar_subcommand(
                            sys.argv[2], JOB_LIST))
                        sys.exit(-1)
                except IndexError as e:
                    logger.error(
                        f"Please provide \"yeedu job [-h] [job-services]\"\n")
                    sys.exit(-1)

            elif sys.argv[1] == 'iam':
                try:
                    if (sys.argv[2] in IAM_LIST) or (sys.argv[2] in ['-h', '--help']):
                        # IAM
                        parser, subparser = main_parser(sys.argv[1])
                        ServiceParser.create_service_parser(
                            sys.argv[1], subparser)
                        call_service_subcommand(parser, sys.argv[1])
                    else:
                        logger.error(
                            f"Please provide \"yeedu iam [iam-service]\"\n")
                        logger.error(get_similar_subcommand(
                            sys.argv[2], IAM_LIST))
                        sys.exit(-1)
                except IndexError as e:
                    logger.error(
                        f"Please provide \"yeedu iam [-h] [iam-services]\"\n")
                    sys.exit(-1)

            elif sys.argv[1] == 'admin':
                try:
                    if (sys.argv[2] in ADMIN_LIST) or (sys.argv[2] in ['-h', '--help']):
                        # ADMIN
                        parser, subparser = main_parser(sys.argv[1])
                        ServiceParser.create_service_parser(
                            sys.argv[1], subparser)
                        call_service_subcommand(parser, sys.argv[1])
                    else:
                        logger.error(
                            f"Please provide \"yeedu admin [admin-service]\"\n")
                        logger.error(get_similar_subcommand(
                            sys.argv[2], ADMIN_LIST))
                        sys.exit(-1)
                except IndexError as e:
                    logger.error(
                        f"Please provide \"yeedu admin [-h] [admin-services]\"\n")
                    sys.exit(-1)

            elif sys.argv[1] == 'platform-admin':
                try:
                    if (sys.argv[2] in PLATFORM_ADMIN_LIST) or (sys.argv[2] in ['-h', '--help']):
                        # PLATFORM ADMIN
                        parser, subparser = main_parser(sys.argv[1])
                        ServiceParser.create_service_parser(
                            sys.argv[1], subparser)
                        call_service_subcommand(parser, sys.argv[1])
                    else:
                        logger.error(
                            f"Please provide \"yeedu platform-admin [platform-admin-service]\"\n")
                        logger.error(get_similar_subcommand(
                            sys.argv[2], PLATFORM_ADMIN_LIST))
                        sys.exit(-1)
                except IndexError as e:
                    logger.error(
                        f"Please provide \"yeedu platform-admin [-h] [platform-admin-services]\"\n")
                    sys.exit(-1)

            elif sys.argv[1] == 'configure':
                try:
                    # Configure
                    parser = main_parser(sys.argv[1])
                    ConfigureUserParser.configure_user_parser(parser)
                    call_service_subcommand(parser)

                except IndexError as e:
                    logger.error(
                        f"Please provide \"yeedu configure [-h] [configure-options]\"\n")
                    sys.exit(-1)

            elif sys.argv[1] == 'logout':
                try:
                    # Configure
                    parser = main_parser(sys.argv[1])
                    ConfigureUserParser.user_logout_parser(parser)
                    call_service_subcommand(parser)

                except IndexError as e:
                    logger.error(
                        f"Please provide \"yeedu logout [-h] [logout-options]\"\n")
                    sys.exit(-1)

            elif sys.argv[1] in ['-h', '--help']:
                logger.info(
                    "\nyeedu configure [-h] [configure-options]\nyeedu resource [-h] [resource-services]\nyeedu cluster [-h] [cluster-services]\nyeedu job [-h] [job-services]\nyeedu iam [-h] [iam-services]\nyeedu admin [-h] [admin-services]\nyeedu platform-admin [-h] [platform-admin-services]\nyeedu logout [-h] [logout-options]\n")

            elif sys.argv[1] in ['-v']:
                logger.info("yeedu 1.0.0\n")

            else:
                logger.error(
                    f"""usage:\tyeedu [-v]\n\tyeedu configure [-h] [configure-options]\n\tyeedu resource [-h] [resource-services]\n\tyeedu cluster [-h] [cluster-services]\n\tyeedu job [-h] [job-services]\n\tyeedu iam [-h] [iam-services]\n\tyeedu admin [-h] [admin-services]\n\tyeedu platform-admin [-h] [platform-admin-services]\n\tyeedu logout [-h] [logout-options]\n\nyeedu: error: argument command: {sys.argv[1]} \nInvalid choice, valid choices are:\n configure | resource | cluster | job | iam | admin | platform-admin | logout""")
        else:
            logger.error("""usage: yeedu [-v]
       yeedu [-h]
       yeedu configure [-h] [configure-options]
       yeedu resource [-h] [resource-services]
       yeedu cluster [-h] [cluster-services]
       yeedu job [-h] [job-services]
       yeedu iam [-h] [iam-services]
       yeedu admin [-h] [admin-services]
       yeedu platform-admin [-h] [platform-admin-services]
       yeedu logout [-h] [logout-options]\n""")
            sys.exit(-1)
    except Exception as e:
        logger.exception(e)
        sys.exit(-1)


def main_parser(service):
    try:
        parser = ArgumentParser(
            description="Yeedu CLI",
            usage=SUPPRESS,
            add_help=False,
            formatter_class=ArgumentDefaultsHelpFormatter
        )

        parser.add_argument(
            "yeedu",
            type=str,
            choices=[service]
        )
        parser.add_argument(
            '-h', '--help',
            action='help',
            default=SUPPRESS,
            help='Show this help message and exit.'
        )

        if service in ['configure', 'logout']:
            return parser
        else:
            subparser = parser.add_subparsers(dest='subcommand')
            return parser, subparser

    except Exception as e:
        logger.exception(e)
        sys.exit(-1)


def call_service_subcommand(parser, command=None):
    try:
        args = parser.parse_args()

        if args.yeedu in ['configure', 'logout']:
            ServiceSubcommand.call_configure_service_subcommand(args)
        elif args.subcommand in RESOURCE_LIST:
            ServiceSubcommand.call_resource_service_subcommand(args)
        elif args.subcommand in CLUSTER_LIST and command == 'cluster':
            ServiceSubcommand.call_cluster_service_subcommand(args)
        elif args.subcommand in JOB_LIST and command == 'job':
            ServiceSubcommand.call_job_service_subcommand(args)
        elif args.subcommand in IAM_LIST and command == 'iam':
            ServiceSubcommand.call_iam_service_subcommand(args)
        elif args.subcommand in ADMIN_LIST and command == 'admin':
            ServiceSubcommand.call_common_platform_and_admin_service_subcommand(
                args)
        elif args.subcommand in PLATFORM_ADMIN_LIST and command == 'platform-admin':
            ServiceSubcommand.call_common_platform_and_admin_service_subcommand(
                args)
        else:
            logger.error(f"{args.subcommand} Not found in any yeedu services.")
            sys.exit(-1)

    except Exception as e:
        logger.exception(e)
        sys.exit(-1)


if __name__ == '__main__':
    yeedu()
