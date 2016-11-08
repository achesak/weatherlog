# -*- coding: utf-8 -*-


################################################################################
#
# WeatherLog: constants.py
# This moduledefines constants used by the rest of the application.
#
################################################################################


__all__ = ["SelectionMode", "DialogResponse", "ImportValidation", "DateValidation", "PastebinExport", "DatasetSelectionMode",
           "ImportType", "DatasetColumn", "WeatherCondition", "CloudCoverageType", "InfoType", "DatasetValidation"]


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
    SELECT_ALL = 18
    REMOVE_ALL = 19
    IMPORT_ALL = 20
    IMPORT = 21
    IMPORT_OVERWRITE = 22
    MOVE_DATA = 34
    COPY_DATA = 35
    USE_NEW = 40
    USE_SELECTED = 41
    EXPORT_JSON = 97
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


# Dataset validation values:
class DatasetValidation:
    VALID = 1
    BLANK = 2
    ALL_SPACE = 3
    LEADING_PERIOD = 4
    CONTAINS_SYMBOL = 5
    IN_USE = 6


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
    SUNNY = [800, 904, 951]
    CLOUDY = [804]
    CLEAR_NIGHT = []
    PARTLY_CLOUDY = [801, 802, 803]
    FOG = [701, 711, 721, 741, 751, 761, 762]
    WIND = [731, 771, 781, 900, 901, 902, 905, 952, 953, 954, 955, 956, 957, 958, 959, 962]
    RAIN = [302, 312, 313, 314, 501, 520, 521, 531]
    RAIN_LIGHT = [300, 301, 310, 311, 321, 500]
    RAIN_HEAVY = [502, 503, 504, 511, 522, 906]
    THUNDERSTORM = [200, 201, 210, 211, 230, 231, 960]
    THUNDERSTORM_HEAVY = [202, 212, 232, 961]
    MIXED = [615, 616]
    SNOW = [601, 611, 612, 621, 903]
    SNOW_LIGHT = [600, 620]
    SNOW_HEAVY = [602, 622]


# Cloud coverage types:
class CloudCoverageType:
    SUNNY = 0
    MOSTLY_SUNNY = 1
    PARTLY_CLOUDY = 2
    MOSTLY_CLOUDY = 3
    CLOUDY = 4


# Info types:
class InfoType:
    INFO = 0
    CHART = 1
    GRAPH = 2
