# -*- coding: utf-8 -*-
# !/usr/bin/env python

# Python imports
import os


###############################
# SECTION: BROWSERS UTILITIES #
###############################

# List of user installed browsers.
# This list is used to simplify browsers recognition.
# E.g. "Google Chrome" will be referred to as "chrome" to avoid any mismatch with names within the application.
USER_INSTALLED_BROWSERS = ["chrome", "firefox", "opera"]

# Windows registry keys for Internet Explorer
IEXPLORER_KEY = r"SOFTWARE\Microsoft\Internet Explorer"
IEXPLORER_MAIN_KEY = r"SOFTWARE\Microsoft\Internet Explorer\Main"

# Windows registry key containing Microsoft Edge
PACKAGES_KEY = r"SOFTWARE\Classes\Local Settings\Software\Microsoft\Windows\CurrentVersion\AppModel\Repository\Packages"

# Uninstall registry key (For user installed browsers)
UNINSTALL_KEY = r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall"

# Icons path
ICONS_PATH = os.path.join(os.path.dirname(__file__), "..", "gui", "icons")

# Browsers cache default paths
BROWSERS_DEFAULT_CACHE_PATHS = {

    ("chrome", "windows", "10"): os.path.join("C:", os.sep, "Users", unicode(os.environ['USERNAME']),
                                              "AppData", "Local", "Google", "Chrome", "User Data", "Default", "Cache"),

    ("firefox", "windows", "10"): "",

    ("opera", "windows", "10"): "",

    ("explorer", "windows", "10"): "",

    ("edge", "windows", "10"): ""

}

###################################
# SECTION: CACHE PATH CORRECTNESS #
###################################


def check_valid_cache_path(browser, cache_path):
    """
        Checking if a selected cache path is valid for selected browser.
        To be considered valid, a path must contain specific files (according to the browser).
        :param browser: Selected browser
        :param cache_path: Cache path for selected browser
        :return: True or false for valid or not not cache path
        """

    # Existing path
    if os.path.exists(cache_path):
        # Google Chrome
        if browser == "chrome":
            # Chrome index and data_ files
            chrome_files = ["index", "data_0", "data_1", "data_2", "data_3"]
            # All files in "chrome_files" are in cache folder
            if set(chrome_files).issubset(os.listdir(cache_path)):
                return True
            # Not all files in "chrome_files" are in cache folder
            return False
    # Not existing path
    else:
        return False
