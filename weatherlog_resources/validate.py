# -*- coding: utf-8 -*-


################################################################################
#
# WeatherLog: validate.py
# This module validates user-entered data.
#
################################################################################


# Import re for pattern matching.
import re
# Import os.path for checking if a directory exists.
import os.path

# Import application modules.
from weatherlog_resources.constants import *
import weatherlog_resources.io as io


validate_dataset_strings = {
    ImportValidation.VALID: "No error, this should never display.",
    ImportValidation.NOT_LIST: "Data is not a list.",
    ImportValidation.NOT_SUBLIST: "One or more items in the data are not lists.",
    ImportValidation.INCORRECT_LENGTH: "One or more lists do not have the correct length.",
    ImportValidation.NOT_STRING: "One or more data fields are not strings.",
    ImportValidation.CANNOT_UNPICKLE: "The file is not in the correct format.",
    ImportValidation.NO_DATA: "The file contains no data."
}

validate_dataset_name_strings = {
    DatasetValidation.VALID: "No error, this should never display.",
    DatasetValidation.BLANK: "Dataset names cannot be blank.",
    DatasetValidation.ALL_SPACE: "Dataset names cannot be all space.",
    DatasetValidation.LEADING_PERIOD: "Dataset names cannot begin with a period.",
    DatasetValidation.CONTAINS_SYMBOL: "Dataset names can only contain letters, numbers, and spaces.",
    DatasetValidation.IN_USE: "Dataset name is already in use."
}


def validate_dataset(main_dir, name):
    """Validates a dataset name."""
    
    if not name:
        return DatasetValidation.BLANK
    elif name.lstrip().rstrip() == "":
        return DatasetValidation.ALL_SPACE
    elif name.startswith("."):
        return DatasetValidation.LEADING_PERIOD
    elif re.compile("[^a-zA-Z1-90 \.\-\+\(\)\?\!]").match(name):
        return DatasetValidation.CONTAINS_SYMBOL
    elif os.path.isdir("%s/datasets/%s" % (main_dir, name)):
        return DatasetValidation.IN_USE
    else:
        return DatasetValidation.VALID


def validate_data(filename):
    """Validates imported data."""
    
    # Test 1: must be readable.
    try:
        data = io.read_dataset(filename = filename)
    except:
        return ImportValidation.CANNOT_UNPICKLE
    
    # Test 2: must be a list.
    if not isinstance(data, list):
        return ImportValidation.NOT_LIST
    
    # Test 3: each item must be a list.
    # Test 4: each item must have the correct length (10).
    # Test 5: each item of this list must be a string.
    for i in data:
        if not isinstance(i, list):
            return ImportValidation.NOT_SUBLIST
        if len(i) != 10:
            return ImportValidation.INCORRECT_LENGTH
        for j in i:
            if not isinstance(j, str):
                return ImportValidation.NOT_STRING
    
    return ImportValidation.VALID
