"""Command-line utility for executing Django administrative tasks."""

import os
import sys

from django.core.management import execute_from_command_line


def main() -> None:
    """Parse the commandline and run administrative tasks"""

    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'keystone_status.main.settings')
    execute_from_command_line(sys.argv)
