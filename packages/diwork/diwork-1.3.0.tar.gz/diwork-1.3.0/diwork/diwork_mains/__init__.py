# -*- coding: utf-8 -*-

# For pycharm: Setting -> Project -> Project Structure ->
#                           Mark as source all folders contains src

from .diwork_hash import main_hash
from .diwork_clone import main_clone
from .diwork_diff import main_diff
from .diwork_difx import main_difx
from .diwork_repeats import main_repeats
from .diwork_exec import main_exec
from .diwork_help import main_help
from .diwork_sshclone import main_sshclone
from .diwork_archive import main_archive
from .diwork_diffclone import main_diffclone

__all__ = [
    "main_help",
    "main_hash",
    "main_clone",
    "main_diff",
    "main_difx",
    "main_repeats",
    "main_exec",
    "main_sshclone",
    "main_archive",
    "main_diffclone"
]
