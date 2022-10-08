"""
Constant types in Python.

import const

const.FOO = 100
const.FOO = 200  # const.ConstError: Can't rebind const (HOGE)
"""

class _const:
    class ConstError(TypeError):
        pass

    def __setattr__(self, name, value):
        if name in self.__dict__:
            raise self.ConstError("Can't rebind const (%s)" % name)
        self.__dict__[name] = value

import sys
sys.modules[__name__]=_const()