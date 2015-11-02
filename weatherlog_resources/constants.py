# -*- coding: utf-8 -*-


# This file defines constants used by other parts of the application.


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


# Import validation values: TODO: hook this up for validate.validate_data()
class ImportValidation:
    VALID = 1
    NOT_LIST = 0
    NOT_SUBLIST = -1
    INCORRECT_LENGTH = -2
    NOT_STRING = -3
