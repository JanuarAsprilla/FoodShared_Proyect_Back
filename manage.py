#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
from django.urls import get_resolver


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'foodshared_project.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()


def print_urls(url_patterns, prefix=''):
    for pattern in url_patterns:
        if hasattr(pattern, 'url_patterns'):  # Verifica si hay subpatrones
            print_urls(pattern.url_patterns, prefix + pattern.pattern.regex.pattern)
        else:
            print(f'{prefix}{pattern.pattern} --> {pattern.callback}')

if __name__ == "__main__":
    resolver = get_resolver()
    print_urls(resolver.url_patterns)
