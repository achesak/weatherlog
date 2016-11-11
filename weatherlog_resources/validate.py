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
# Import pickle for loading and saving the data.
try:
    import cPickle as pickle
except ImportError:
    import pickle

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
    
    # Test 1: must not be blank
    if not name:
        return DatasetValidation.BLANK

    # Test 2: must not be all space
    elif name.lstrip().rstrip() == "":
        return DatasetValidation.ALL_SPACE

    # Test 3: must not start with a period; this can cause issues on Unix-based systems.
    elif name.startswith("."):
        return DatasetValidation.LEADING_PERIOD

    # Test 4: must not contain invalid symbol.
    elif re.compile("[/\\\\]").match(name):
        return DatasetValidation.CONTAINS_SYMBOL

    # Test 5: must not be in use.
    elif os.path.isdir("%s/datasets/%s" % (main_dir, name)):
        return DatasetValidation.IN_USE

    # Otherwise, valid.
    else:
        return DatasetValidation.VALID


def validate_data(filename):
    """Validates imported data."""
    
    # Test 1: must be readable.
    try:
        data = io.read_dataset(filename = filename)
    except pickle.PickleError:
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
