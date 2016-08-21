# -*- coding: utf-8 -*-


# This file defines the functions for command line features.


# Import modules for working with directories.
import shutil, os, os.path
# Import application modules.
import weatherlog_resources.launch as launch


def purge():
    """purge: deletes all program files."""
    
    main_dir, conf_dir = launch.get_main_dir()
    if os.path.exists(main_dir):
        shutil.rmtree(main_dir)
    if os.path.exists(conf_dir):
        shutil.rmtree(conf_dir)
    print("All data deleted.")
