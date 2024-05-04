import argparse
from . import Assets, __version__

assets = Assets()


def cli() -> None:
    parser = argparse.ArgumentParser(
        description="Install 'Chrome for Testing' assets",
        epilog='Reference: https://github.com/GoogleChromeLabs/'
               +'chrome-for-testing'
    )

    parser.add_argument(
        '-V',
        '--version',
        action='version',
        version=f'v{__version__}',
        help='Show version and exit.'
    )

    sub_parsers = parser.add_subparsers(
        title='Commands',
        dest='command'
    )

    help_install = "Install a version of 'Chrome for Testing' assets"
    sp_install = sub_parsers.add_parser(
        'install',
        description=help_install,
        help=help_install
    )
    sp_install.add_argument(
        '--version',
        default='latest',
        help="The version of 'Chrome for Testing' assets to install. " +
             "The default is '%(default)s'"
    )
    sp_install.add_argument(
        '-l',
        '--last-known-good-version',
        action='store_true',
        help='Install a last known good version from a list'
    )

    help_path = 'Show the installation path of assets and exit'
    sub_parsers.add_parser(
        'path',
        description=help_path,
        help=help_path
    )

    help_list = 'List versions'
    sp_list = sub_parsers.add_parser(
        'list',
        description=help_list,
        help=help_list
    )
    sp_list.add_argument(
        '-a',
        '--active',
        action='store_true',
        help="List the currently active version of 'Chrome for Testing' assets"
             + " installed."
    )
    sp_list.add_argument(
        '-i',
        '--installed',
        action='store_true',
        help='List installed versions'
    )
    sp_list.add_argument(
        '-l',
        '--last-known-good-versions',
        action='store_true',
        help='List last known good versions'
    )

    help_switch = 'Switch the active version'
    sub_parsers.add_parser(
        'switch',
        description=help_switch,
        help=help_switch
    )

    help_delete = 'Delete an installed version'
    sub_parsers.add_parser(
        'delete',
        description=help_delete,
        help=help_delete
    )

    args = parser.parse_args()

    if args.command == 'install':
        if args.last_known_good_version:
            assets.install_last_known_good_version()
        else:
            print(f"Installing version '{args.version}'")
            assets.install(version=args.version)

    if args.command == 'path':
        print(f'Path to assets: {assets.path}')

    if args.command == 'list':
        if args.installed:
            assets.installed()
        if args.active:
            print("Active version of 'Chrome for Testing' assets installed: "
                + f'{assets.active_version}'
        )
        if args.last_known_good_versions:
            assets.last_known_good_versions()

    if args.command == 'switch':
        assets.switch()

    if args.command == 'delete':
        assets.delete()
