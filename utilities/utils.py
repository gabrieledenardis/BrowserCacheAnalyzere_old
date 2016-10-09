# -*- coding: utf-8 -*-
# !/usr/bin/env python

# Python imports
import os
import datetime
import hashlib


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

#############################
# SECTION: TIME CONVERSIONS #
#############################


def webkit_to_unix_timestamp(webkit_time):
    """
    Convert from webkit timestamp to unix time stamp.
    :param webkit_time: Chrome file creation time (Read within index file)
    :return: Time in readable format
    """
    # From webkit time in microseconds to webkit time in seconds
    microsec_in_sec = float(1000000)
    webkit_time_microsec = float(int(webkit_time, 0))
    webkit_time_sec = webkit_time_microsec / microsec_in_sec

    # Webkit and unix starting date
    webkit_time_start = datetime.datetime(1601, 1, 1)
    unix_time_start = datetime.datetime(1970, 1, 1)

    # Delta time in seconds between webkit and unix starting date
    delta_starting_dates_seconds = (unix_time_start - webkit_time_start).total_seconds()

    # Correct timestamp in unix time
    correct_timestamp = webkit_time_sec - delta_starting_dates_seconds

    # Unix timestamp in readable time
    readable_time = datetime.datetime.fromtimestamp(correct_timestamp).strftime("%A - %d %B %Y - %H:%M:%S")

    return readable_time

#########################
# SECTION: FILE HASHING #
#########################


def file_cryptography(file_path):
    """
    Calculating md5 and sha1 for selected file from list folder widget.
    :param file_path: Selected file path of selected item in "list input folder" widget.
    :return: File md5 and sha1.
    """
    hash_md5 = hashlib.md5()
    hash_sha1 = hashlib.sha1()
    buf_dimension = 65536

    with open(file_path, 'rb') as f:
        while True:
            buf = f.read(buf_dimension)
            if not buf:
                break
            hash_md5.update(buf)
            hash_sha1.update(buf)
    md5 = hash_md5.hexdigest()
    sha1 = hash_sha1.hexdigest()

    results = {'md5': md5, 'sha1': sha1}

    return results

