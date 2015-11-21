# -*- coding: utf-8 -*-


# This file defines functions for validating user-entered data.


# Import constants.
from weatherlog_resources.constants import *
# Import re for pattern matching.
import re
# Import os.path for checking if a directory exists.
import os.path


def validate_profile(main_dir, name):
    """Validates a profile name."""
    
    if not name:
        return "The dataset name \"%s\" is not valid. Dataset names may not be blank."
    elif name.lstrip().rstrip() == "":
        return "The dataset name \"%s\" is not valid. Dataset names may not be all spaces."
    elif name.startswith("."):
        return "The dataset name \"%s\" is not valid. Dataset names may not start with a period."
    elif re.compile("[^a-zA-Z1-90 \.\-\+\(\)\?\!]").match(name):
        return "The dataset name \"%s\" is not valid. Dataset names may only be letters, numbers, and spaces."
    elif os.path.isdir("%s/profiles/%s" % (main_dir, name)):
        return "The dataset name \"%s\" is already in use." % name
    else:
        return ""


def validate_data(data):
    """Validates imported data."""
    
    # Test 1: must be a list.
    if not isinstance(data, list):
        return ImportValidation.NOT_LIST
    
    # Test 2: each item must be a list.
    # Test 3: each item must have the correct length (10).
    # Test 4: each item of this list must be a string.
    for i in data:
        if not isinstance(i, list):
            return ImportValidation.NOT_SUBLIST
        if len(i) != 10:
            return ImportValidation.INCORRECT_LENGTH
        for j in i:
            if not isinstance(j, str):
                return ImportValidation.NOT_STRING
    
    return ImportValidation.VALID
