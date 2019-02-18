import argparse


def getOptions(args):
    parser = argparse.ArgumentParser(
        prog='scenery',
        description='Scenery - A pattern-based scene-release renamer.'
    )

    parser.add_argument('path',
                        action='store',
                        help='''Which path to process.
                            If a directory is given, it's scanned recursively and all files are processed.
                            If a file is given, only it is processed.''')

    parser.add_argument('-p', '--pattern',
                        action='store',
                        dest='pattern',
                        default='%a S%sE%n %t',
                        help='''Output format pattern. Syntax:
                            %%a - Show name,
                            %%s - Season #,
                            %%n - Season #,
                            %%t - Episode title
                            (default: %%a S%%sE%%n %%t)''')

    parser.add_argument('-s', '--season-zeroes',
                        action='store_true',
                        dest='zeroesSeason',
                        help='Leading zeroes in season numbers')

    parser.add_argument('-e', '--episode-zeroes',
                        action='store_true',
                        dest='zeroesEpisodes',
                        help='Leading zeroes in episode numbers')

    parser.add_argument('-o', '--overwrite',
                        action='store_true',
                        dest='overwrite',
                        help='Overwrite existing target files')

    parser.add_argument('-d', '--dry-run',
                        action='store_true',
                        dest='dryRun',
                        help='Do not do the actual renaming, but just show what would happen instead')

    parser.add_argument('-v', '--verbose',
                        action='store_true',
                        dest='verbose',
                        help='Output successful actions as well')

    parser.add_argument('-f', '--force',
                        action='store_true',
                        dest='force',
                        help="Rename files even if the show name couldn't be resolved")

    return parser.parse_args(args)
