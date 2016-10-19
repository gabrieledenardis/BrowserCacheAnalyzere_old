# -*- coding: utf-8 -*-
# !/usr/bin/env python

# Python imports
import os
import datetime
import hashlib
import psutil
import platform


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


###############################
# SECTION: CHECK OPEN BROWSER #
###############################

def check_open_browser(browser):
    """
    Slot for "next" button in "browser choice screen".
    Checking if selected browser is open.
    :param browser: Browser key for selected browser (E.g. "chrome" for "Google Chrome").
    :return: True or false for open or not browser
    """

    # Searching for browser process in open processes
    for process in psutil.process_iter():
        # Browser key found in a process name
        if browser in process.name():
            return True
    # Browser key not found in a process name
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


########################
# SECTION: FOLDER INFO #
########################

def get_folder_info(folder_path):
    """

    :param folder_path:
    :return: results
    """

    folder_dimension = 0
    for dir_path, dir_names, file_names in os.walk(folder_path):
        for f in file_names:
            fp = os.path.join(dir_path, f)
            folder_dimension += os.path.getsize(fp)

    # Other values for selected folder
    folder_elements = len(os.listdir(folder_path))
    folder_creation_time = os.stat(folder_path).st_ctime
    folder_last_access_time = os.stat(folder_path).st_atime
    readable_creation_time = datetime.datetime.fromtimestamp(folder_creation_time) \
        .strftime("%A - %d %B %Y - %H:%M:%S")
    readable_last_access_time = datetime.datetime.fromtimestamp(folder_last_access_time) \
        .strftime("%A - %d %B %Y - %H:%M:%S")

    results = {'folder_dimension': folder_dimension, 'folder_elements': folder_elements,
               'folder_creation_time': readable_creation_time, 'folder_last_access_time': readable_last_access_time}

    return results


######################
# SECTION: FILE INFO #
######################

def get_file_info(file_path):
    """

    :param file_path:
    :return:
    """

    # File info
    file_dimension = os.stat(file_path).st_size
    creation_time = os.stat(file_path).st_ctime
    last_modified_time = os.stat(file_path).st_mtime
    last_access_time = os.stat(file_path).st_atime

    # Readable times
    creation_time_readable = datetime.datetime.fromtimestamp(creation_time).strftime("%A - %d %B %Y - %H:%M:%S")
    last_modified_time_readable = datetime.datetime.fromtimestamp(last_modified_time)\
        .strftime("%A - %d %B %Y - %H:%M:%S")
    last_access_time_readable = datetime.datetime.fromtimestamp(last_access_time) \
        .strftime("%A - %d %B %Y - %H:%M:%S")

    # Hash
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

    results = {'file_dimension': file_dimension, 'creation_time': creation_time_readable,
               'last_modified': last_modified_time_readable, 'last_access': last_access_time_readable, 'md5': md5,
               'sha1': sha1}

    return results

