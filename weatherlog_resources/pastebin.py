# -*- coding: utf-8 -*-


# This file defines functions used for uploading data to pastebin.


# Import urlopen and urlencode for making requests.
try:
    from urllib.request import urlopen
    from urllib.parse import urlencode
except ImportError:
    from urllib import urlopen, urlencode
# Import json and export for converting data format.
import json
import weatherlog_resources.export as export
# Import application constants.
from weatherlog_resources.constants import *


def upload_pastebin(data, name, mode, units, config):
    """Uploads the data to pastebin."""
    
    # Convert the data.
    if mode == "html":
        new_data = export.html(data, units)
    elif mode == "csv":
        new_data = export.csv(data, units)
    elif mode == "json":
        new_data = json.dumps(data)
    
    # Build the api string.
    api = {"api_option": "paste",
           "api_dev_key": config["pastebin"],
           "api_paste_code": new_data}
    if mode == "html":
        api["api_paste_format"] = "html5"
    elif mode == "raw":
        api["api_paste_format"] = "javascript"
    if name.lstrip().rstrip() != "":
        api["api_paste_name"] = name.lstrip().rstrip()
    
    # Upload the text.
    try:
        pastebin = urlopen("http://pastebin.com/api/api_post.php", urlencode(api))
        result = pastebin.read()
        pastebin.close()
        
        # Check for an error message.
        if "invalid api_dev_key" in result:
            return PastebinExport.INVALID_KEY, False
        else:
            return PastebinExport.SUCCESS, result
        
    except:
        return PastebinExport.ERROR, False
