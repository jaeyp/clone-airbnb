import sys


class _constant:
    def __setattr__(self, name, value):
        if True:
            raise Exception("Can't assign a value.")
        else:  # allow to initialize once
            if name in self.__dict__:
                raise Exception("Can't assign a value.")
            self.__dict__[name] = value

    def __delattr__(self, name):
        if name in self.__dict__:
            raise Exception("Can't delete a variable.")

    """ CONST DEFINITIONS
        Restart server when it's changed
        """
    PAGINATE_BY = 8
    PAGINATE_ORPHANS = 1


sys.modules[__name__] = _constant()

""" for runtime value testing
    comment class code and uncomment below
    """
# PAGINATE_BY = 8
# PAGINATE_ORPHANS = 3
