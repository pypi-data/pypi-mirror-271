import typing

GenericType = typing.TypeVar("GenericType")

class JunctionModuleHandle:
    """ """

    def register_module(self):
        """ """
        ...

    def register_submodule(self, submodule_name, dirpath):
        """

        :param submodule_name:
        :param dirpath:
        """
        ...

    def rename_directory(self, submodule_name, dirpath):
        """

        :param submodule_name:
        :param dirpath:
        """
        ...

    def rename_submodule(self, submodule_name_src, submodule_name_dst):
        """

        :param submodule_name_src:
        :param submodule_name_dst:
        """
        ...

    def submodule_items(self):
        """ """
        ...

    def unregister_module(self):
        """ """
        ...

    def unregister_submodule(self, submodule_name):
        """

        :param submodule_name:
        """
        ...
