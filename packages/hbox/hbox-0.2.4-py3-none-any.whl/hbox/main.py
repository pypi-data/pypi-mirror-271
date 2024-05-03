import logging
from hbox import config
from hbox.logger import set_log_level


def setup_logger():
    cfg = config.load_config()
    set_log_level(logging.DEBUG if cfg.debug else logging.INFO)


def run():
    setup_logger()

    import argparse
    from hbox.commands import (
        add_package,
        list_packages,
        remove_package,
        run_package,
        show_info,
        set_package_version,
        show_version
    )

    parser = argparse.ArgumentParser(description="CLI tool that leverages container technology to manage packages.")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    subparsers.add_parser("info", help="Print debug information.")

    subparsers.add_parser("version", help="Show current hbox version.")

    parser_list = subparsers.add_parser("list", help="List all installed packages and their versions.")
    parser_list.add_argument("name", type=str, nargs='?', default=None, help="Show all versions for a given package.")

    parser_add = subparsers.add_parser("add", help="Add a specific version of a package", aliases=['install'])
    parser_add.add_argument("name", type=str, help="Name of the package to install")
    parser_add.add_argument("version", nargs="?", type=str, default="latest",
                            help="Version of the package (default: latest)")
    parser_add.add_argument("-d", "--set-default", action="store_true",
                            help="Set the added version as the current version")

    parser_remove = subparsers.add_parser('remove', help='Remove a package.', aliases=['uninstall'])
    parser_remove.add_argument('name', help='The name of the package to remove.')
    parser_remove.add_argument("version", nargs="?", type=str, default=None,
                               help="Version of the package (default: latest)")

    parser_run = subparsers.add_parser("run", help="Run the package.")
    parser_run.add_argument("name", type=str, help="Name of the package to run")
    parser_run.add_argument("subcommand", nargs=argparse.REMAINDER, help="Arguments to pass to the package")

    parser_set = subparsers.add_parser("use", help="Set current version of a package.", aliases=["set"])
    parser_set.add_argument("name", type=str, help="Name of the package to set the version of.")
    parser_set.add_argument("version", type=str, help="New version to set as current.")

    args = parser.parse_args()

    if args.command is None:
        parser.print_help()
    elif args.command == "info":
        show_info()
    elif args.command == "version":
        show_version()
    elif args.command == "list":
        list_packages(args.name)
    elif args.command in ["add", "install"]:
        add_package(args.name, args.version, args.set_default)
    elif args.command in ["remove", "uninstall"]:
        remove_package(args.name, args.version)
    elif args.command in ["use", "set"]:
        set_package_version(args.name, args.version)
    elif args.command == "run":
        run_package(args.name, args.subcommand)


if __name__ == "__main__":
    run()
