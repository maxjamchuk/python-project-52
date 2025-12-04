#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
import subprocess


def main() -> None:
    """Run administrative tasks."""
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "task_manager.settings")

    try:
        import django  # noqa: F401  # просто проверка наличия
    except ImportError:
        if os.getenv("MANAGE_PY_UV_RUN") != "1":
            os.environ["MANAGE_PY_UV_RUN"] = "1"
            cmd = ["uv", "run", "python", "manage.py", *sys.argv[1:]]
            os.execvp("uv", cmd)
        raise

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
