#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

    try:
        from django.core import management  # noqa: WPS433, F401
    except ImportError:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and " +
            'available on your PYTHONPATH environment variable? Did you ' +
            'forget to activate a virtual environment?',
        )

    execute_from_command_line(sys.argv)  # noqa: F821


if __name__ == '__main__':
    main()
