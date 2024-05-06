import importlib

from release_by_changelog.app import app

__all__ = ["app"]

importlib.import_module("release_by_changelog.cmds.release")
