"""
Module containing all config item resolvers for **nmk-doc** plugin.
"""

from datetime import date

from nmk.model.resolver import NmkIntConfigResolver
from nmk_base.resolvers import FilesResolver


class NmkDocInputsResolver(FilesResolver):
    """
    Resolves all files in doc folder
    """

    @property
    def folder_config(self) -> str:
        """
        Tells **FilesResolver** to search files in **${docPath}** config item.
        """
        return "docPath"


class NmkDocYearResolver(NmkIntConfigResolver):
    """
    Current year resolver
    """

    def get_value(self, name: str) -> int:
        """
        Get today's year.

        :param name: config item name to be resolved
        :return: current year
        """

        # Today's year
        return date.today().year
