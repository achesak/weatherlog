# -*- coding: utf-8 -*-


# This file defines constants used by other parts of the application.


__all__ = ["SelectionMode", "DialogResponse", "ImportValidation"]


# Data subset selection mode:
class SelectionMode:
    ALL = 0
    ONE = 1
    NONE = 2


# Dialog response values:
class DialogResponse:
    RESET = 3
    EXPORT = 9
    ADD_DATA = 10
    IMPORT_ALL = 20
    IMPORT = 21
    MOVE_DATA = 34
    EXPORT_CSV = 98
    EXPORT_HTML = 99


# Import validation values:
class ImportValidation:
    VALID = 1
    NOT_LIST = 0
    NOT_SUBLIST = -1
    INCORRECT_LENGTH = -2
    NOT_STRING = -3
    CANNOT_UNPICKLE = -4
    NO_DATA = -5
