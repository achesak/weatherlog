# -*- coding: utf-8 -*-


# This file defines functions for validating user-entered data.


# Import re for pattern matching.
import re
# Import os.path for checking if a directory exists.
import os.path


def validate_profile(main_dir, name):
    """Validates a profile name."""
    
    if re.compile("[^a-zA-Z1-90 \.\-\+\(\)\?\!]").match(name) or not name or name.lstrip().rstrip() == "" or name.startswith("."):
        return "The dataset name \"%s\" is not valid.\n\n1. Dataset names may not be blank.\n2. Dataset names may not be all spaces.\n3. Dataset names may only be letters, numbers, and spaces.\n4. Dataset names may not start with a period (\".\")." % name
    
    elif os.path.isdir("%s/profiles/%s" % (main_dir, name)):
        return "The dataset name \"%s\" is already in use." % name
    
    else:
        return ""


def validate_data(data):
    """Validates imported data.
       Return codes:
       1 - No error, data validated
       0 - Data is not a list
       -1 - Sub-data are not lists
       -2 - Sub-lists must have the correct length
       -3 - Each item in the sub-lists must be a string
    """
    
    # Test 1: must be a list.
    if not isinstance(data, list):
        return 0
    
    # Test 2: each item must be a list.
    # Test 3: each item must have the correct length (10).
    # Test 4: each item of this list must be a string.
    for i in data:
        if not isinstance(i, list):
            return -1
        if len(i) != 10:
            return -2
        for j in i:
            if not isinstance(j, str):
                return -3
    
    return 1
