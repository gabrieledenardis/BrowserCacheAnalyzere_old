# -*- coding: utf-8 -*-
# !/usr/bin/env python

# Python imports
import os


###############################
# SECTION: BROWSERS UTILITIES #
###############################

# List of user supported browsers.
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
