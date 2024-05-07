"""
    This module provides the default settings of the
    package test
"""

from importlib import metadata
from pathlib import Path
import tomlkit

ROOT_DIR = Path(__name__).resolve().parent.parent
DEBUG = True

try:
    package = metadata.metadata('aigents')
    name = package['name']
    version = package['version']
    author = package['author']
    author_email = package['author-email']
    summary = package['summary']
except metadata.PackageNotFoundError:
    # Read metadata from pyproject.toml
    with open(ROOT_DIR / 'pyproject.toml', 'r', encoding='utf-8') as file:
        pyproject_data = tomlkit.parse(file.read())

    poetry_section = pyproject_data.get('tool', {}).get('poetry', {})
    name = poetry_section.get('name')
    version = poetry_section.get('version')
    author = poetry_section.get('authors', [''])[0]
    author_email = ''
    if isinstance(author, str):
        parts = author.split('<')
        if len(parts) == 2:
            author = parts[0].strip()
            author_email = parts[1].strip('>').strip()
    summary = poetry_section.get('description')

DEBUG = True

TITLE = name
DELIMITER = len(TITLE)*"="
HEADER = f"""
{DELIMITER}
{TITLE}
Version: {version}
Description: {summary }
Authors: {author}
{DELIMITER}
"""

CONFIG_LOG = {
    "version": 1,
    "formatters": {
        "client": {"format": "%(levelname)s: %(message)s"},
        "standard": {
            "format": (
                "%(levelname)s (at %(pathname)s - %(funcName)s "
                "in line %(lineno)d): %(message)s"
            )
        },
        "debug": {
            "format": (
                "%(asctime)s %(levelname)s (at %(funcName)s "
                "in line %(lineno)d):"
                "\n\t|──file: %(pathname)s"
                "\n\t|──task name: %(taskName)s"
                "\n\t└──message: %(message)s\n"
            ),
            "datefmt": "%y-%m-%d %H:%M:%S"
        }
    },
    "handlers": {
        "client": {
            "class": "logging.StreamHandler",
            "formatter": "client",
            "level": "INFO"
        },
        "standard": {
            "class": "logging.StreamHandler",
            "formatter": "standard",
            "level": "DEBUG"
        },
        "debug": {
            "class": "logging.StreamHandler",
            "formatter": "debug",
            "level": "DEBUG"
        }
    },
    "root": {"handlers": ["standard"], "level": "DEBUG"},
    "loggers": {
        "client": {
            "handlers": ["client"],
            "level": "DEBUG",
            "propagate": False,
            "disable_existing_loggers": False
        },
        "standard": {
            "handlers": ["standard"],
            "level": "DEBUG",
            "propagate": False,
            "disable_existing_loggers": False
        }
    }
}
