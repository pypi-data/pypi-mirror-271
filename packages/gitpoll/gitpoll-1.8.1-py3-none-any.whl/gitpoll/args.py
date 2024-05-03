# gitpoll/args.py
import os
from argparse import ArgumentParser, Namespace


def parse_args() -> Namespace:
    """Parse command line arguments for the gitpoll application."""
    parser = ArgumentParser(
        description=(
            "Monitors a Git repository for changes and executes "
            + "scripts before and after pulling updates."
        )
    )
    parser.add_argument(
        "repo_path",
        nargs="?",
        help="Path to the Git repository to monitor.",
        default=os.getcwd(),
        type=str,
    )
    parser.add_argument(
        "-i",
        "--interval",
        type=int,
        help="Interval in seconds to check for changes.",
        required=False,
        default=None,
    )
    parser.add_argument(
        "-n",
        "--no-pull",
        action="store_true",
        help="Do not pull changes from the repository.",
        required=False,
    )
    parser.add_argument(
        "-p",
        "--pre-action",
        type=str,
        help="Command or path to the pre-action shell script or command.",
        required=False,
    )
    parser.add_argument(
        "-P",
        "--post-action",
        type=str,
        help="Command or path to the post-action shell script or command.",
        required=False,
    )
    parser.add_argument(
        '-f',
        '--force',
        action='store_true',
        help='Force execution pre and post actions regardless of changes.',
        required=False,
        default=False,
    )

    return parser.parse_args()
