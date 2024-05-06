"""
Helpers for asset management tasks.

"""

import typing

GenericType = typing.TypeVar("GenericType")

class AssetBrowserPanel:
    """ """

    bl_space_type: typing.Any
    """ """

    def asset_browser_panel_poll(self, context):
        """

        :param context:
        """
        ...

    def poll(self, context):
        """

        :param context:
        """
        ...

class AssetMetaDataPanel:
    """ """

    bl_region_type: typing.Any
    """ """

    bl_space_type: typing.Any
    """ """

    def poll(self, context):
        """

        :param context:
        """
        ...

class SpaceAssetInfo:
    """ """

    def get_active_asset(self, context):
        """

        :param context:
        """
        ...

    def is_asset_browser(self, space_data):
        """

        :param space_data:
        """
        ...

    def is_asset_browser_poll(self, context):
        """

        :param context:
        """
        ...
