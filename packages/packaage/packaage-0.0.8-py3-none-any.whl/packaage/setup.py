"""Setup related functions"""
from __future__ import absolute_import

import subprocess


def get_git_branch() -> str:
    """Get the name of the current git branch

    Returns:
        str: The name of the git branch as str

    Example:
    >>> get_git_branch()
    'main'
    """
    return subprocess.check_output(
        ['git', 'rev-parse', '--abbrev-ref', 'HEAD']).strip().decode('utf-8')
