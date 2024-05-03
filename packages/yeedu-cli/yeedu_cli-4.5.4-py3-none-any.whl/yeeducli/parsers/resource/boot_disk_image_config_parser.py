from argparse import SUPPRESS, ArgumentDefaultsHelpFormatter
from yeeducli.constants import CLOUD_PROVIDERS_LIST


class BootDiskImageConfigurationParser:

    def boot_disk_image_config_parser(subparser):
        create_boot_disk_image_conf = subparser.add_parser(
            'create-boot-disk-image-conf',
            help='To create a Boot Disk Image Configuration.',
            formatter_class=ArgumentDefaultsHelpFormatter)
        create_boot_disk_image_conf.add_argument(
            "--cloud_provider_id",
            type=int,
            nargs=1,
            required=True,
            default=SUPPRESS,
            help="Provide boot_disk_image_config to create-boot-disk-image-conf."
        )
        create_boot_disk_image_conf.add_argument(
            "--boot_disk_image",
            type=str,
            nargs=1,
            required=True,
            default=SUPPRESS,
            help="Provide boot_disk_image to create-boot-disk-image-conf."
        )
        create_boot_disk_image_conf.add_argument(
            "--json-output",
            type=str,
            nargs='?',
            choices=['pretty', 'default'],
            default='pretty',
            help="Provide the format of JSON output."
        )
        create_boot_disk_image_conf.add_argument(
            "--yaml-output",
            type=str,
            nargs='?',
            choices=['true', 'false'],
            default='false',
            help="Provide true to get output in YAML format."
        )

        describe_boot_disk_image_conf = subparser.add_parser(
            'get-boot-disk-image-conf',
            help='To get the information about a specific Boot Disk Image Configuration.',
            formatter_class=ArgumentDefaultsHelpFormatter)
        describe_boot_disk_image_conf.add_argument(
            "--boot_disk_image_id",
            type=int,
            nargs=1,
            required=True,
            default=SUPPRESS,
            help="Provide Boot Disk Image Id to get information about a specific Boot Disk Image Configuration."
        )
        describe_boot_disk_image_conf.add_argument(
            "--json-output",
            type=str,
            nargs='?',
            choices=['pretty', 'default'],
            default='pretty',
            help="Provide the format of JSON output."
        )
        describe_boot_disk_image_conf.add_argument(
            "--yaml-output",
            type=str,
            nargs='?',
            choices=['true', 'false'],
            default='false',
            help="Provide true to get output in YAML format."
        )

        list_boot_disk_image_conf = subparser.add_parser(
            'list-boot-disk-image-confs',
            help='To list all the available Boot Disk Image Configurations.',
            formatter_class=ArgumentDefaultsHelpFormatter)
        list_boot_disk_image_conf.add_argument(
            "--cloud_provider",
            type=str,
            nargs='?',
            choices=CLOUD_PROVIDERS_LIST,
            default=SUPPRESS,
            help="Provide cloud_provider to list all the related boot disk image configs for a specific Cloud Provider."
        )
        list_boot_disk_image_conf.add_argument(
            "--json-output",
            type=str,
            nargs='?',
            choices=['pretty', 'default'],
            default='pretty',
            help="Provide the format of JSON output."
        )
        list_boot_disk_image_conf.add_argument(
            "--yaml-output",
            type=str,
            nargs='?',
            choices=['true', 'false'],
            default='false',
            help="Provide true to get output in YAML format."
        )
