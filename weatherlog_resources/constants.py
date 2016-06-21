# -*- coding: utf-8 -*-


# This file defines constants used by other parts of the application.


__all__ = ["SelectionMode", "DialogResponse", "ImportValidation", "DateValidation", "PastebinExport", "DatasetSelectionMode",
           "ImportType", "DatasetColumn", "WeatherCondition"]


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
    IMPORT_OVERWRITE = 22
    MOVE_DATA = 34
    COPY_DATA = 35
    USE_NEW = 40
    USE_SELECTED = 41
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


# Date validation values:
class DateValidation:
	VALID = 1
	INVALID = -1


# Pastebin export values:
class PastebinExport:
    SUCCESS = 0
    INVALID_KEY = 1
    ERROR = 2
    NO_CONSTANTS = 3


# Dataset selection mode:
class DatasetSelectionMode:
    SINGLE = 0
    MULTIPLE = 1


# Import type:
class ImportType:
    MERGE = 0
    OVERWRITE = 0


# Dataset columns:
class DatasetColumn:
    DATE = 0
    TEMPERATURE = 1
    WIND_CHILL = 2
    PRECIPITATION = 3
    WIND = 4
    HUMIDITY = 5
    AIR_PRESSURE = 6
    VISIBILITY = 7
    CLOUD_COVER = 8
    NOTES = 9


# Weather condition codes:
class WeatherCondition:
    SUNNY = [32, 34]
    CLOUDY = [26]
    CLEAR_NIGHT = [31, 33]
    PARTLY_CLOUDY = [27, 28, 29, 30, 44]
    FOG = [19, 20, 21, 22]
    WIND = [23, 24, 0, 2, 15]
    RAIN = [10, 11, 12, 40]
    RAIN_LIGHT = [8, 9]
    RAIN_HEAVY = [1, 6, 17, 18, 35]
    THUNDERSTORM = [4, 37, 38, 39, 45, 47]
    THUNDERSTORM_HEAVY = [3]
    MIXED = [5, 7]
    SNOW = [16, 42, 46]
    SNOW_LIGHT = [13, 14]
    SNOW_HEAVY = [41, 43]
