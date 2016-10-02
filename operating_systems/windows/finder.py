# -*- coding: utf-8 -*-
# !/usr/bin/env python

# Python imports
try:
    import _winreg
except ImportError:
    _winreg = None

# Project imports
from utilities import utils


def browsers_finder(windows_release):
    """
    Looking for installed browsers in system registry.
    For user installed browsers, if values in "user installed browser" list are also in system registry "uninstall" key,
    retrieving values and adding in "found browsers".
    For pre-installed browsers, like "Internet Explorer" or "Microsoft Edge", searching values in their respective
    windows registry keys.
    :param windows_release: release number for Microsoft Windows.
    :return: found_browsers (list of found browsers in the system).
    """

    # Uninstall key (For user installed browsers)
    uninstall_key = None

    # Internet Explorer keys
    iexplorer_key = None
    iexplorer_main_key = None

    # Microsoft Edge keys
    packages_key = None
    edge_key = None

    # Attributes for found browsers
    browser_name = None
    browser_version = None
    browser_path = None

    # List of found browsers in the system
    found_browsers = []

    ####################################
    # SECTION: USER INSTALLED BROWSERS #
    ####################################

    try:
        # Opening uninstall key
        uninstall_key = _winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE, utils.UNINSTALL_KEY, 0, _winreg.KEY_READ)
        # Searching in sub keys of uninstall key for user installed browsers
        for s_k in range(_winreg.QueryInfoKey(uninstall_key)[0]):
            try:
                # Sub key name
                uninstall_sub_key_name = _winreg.EnumKey(uninstall_key, s_k)
                for browser in utils.USER_INSTALLED_BROWSERS:
                    # A browser in "user installed browsers" matches a sub key name
                    if browser in uninstall_sub_key_name.lower():
                        # Matching browser key name
                        browser_key_name = "\\".join([utils.UNINSTALL_KEY, uninstall_sub_key_name])
                        try:
                            # Opening matching browser key
                            browser_key = _winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE, browser_key_name,
                                                          0, _winreg.KEY_READ)
                            # Searching in matching browser key values
                            for val in range(_winreg.QueryInfoKey(browser_key)[1]):
                                try:
                                    # Browser key values
                                    reg_name, reg_value, reg_type = _winreg.EnumValue(browser_key, val)
                                    # Name, version and installation path values
                                    if reg_name == "DisplayName":
                                        browser_name = reg_value
                                    if reg_name == "DisplayVersion":
                                        browser_version = reg_value
                                    if reg_name == "InstallLocation":
                                        browser_path = reg_value
                                except WindowsError as _:
                                    pass
                            # Updating "found browser" list
                            found_browsers.append([browser, browser_name, browser_version, browser_path])
                        except WindowsError as _:
                            pass
                        finally:
                            # Closing matching browser key
                            _winreg.CloseKey(browser_key)
            except WindowsError as _:
                pass
    except WindowsError as _:
        pass
    finally:
        # Closing uninstall key
        _winreg.CloseKey(uninstall_key)

    ##############################
    # SECTION: INTERNET EXPLORER #
    ##############################

    # Internet Explorer version
    try:
        # Opening Internet Explorer key
        iexplorer_key = _winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE, utils.IEXPLORER_KEY, 0, _winreg.KEY_READ)
        # Searching in iexplorer_key values
        for val in range(_winreg.QueryInfoKey(iexplorer_key)[1]):
            try:
                # iexplorer_key values
                reg_name, reg_value, reg_type = _winreg.EnumValue(iexplorer_key, val)
                # Internet Explorer version value
                if reg_name == "svcVersion":
                    browser_version = reg_value
            except WindowsError as _:
                pass
    except WindowsError as _:
        pass
    finally:
        # Closing iexplorer_key
        _winreg.CloseKey(iexplorer_key)

    # Internet Explorer installation path
    try:
        # Opening Internet Explorer Main key
        iexplorer_main_key = _winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE, utils.IEXPLORER_MAIN_KEY, 0, _winreg.KEY_READ)
        #  Searching in iexplorer_main_key values
        for val in range(_winreg.QueryInfoKey(iexplorer_main_key)[1]):
            try:
                # iexplorer_main_key values
                reg_name, reg_value, reg_type = _winreg.EnumValue(iexplorer_main_key, val)
                # Internet Explorer installation path value
                if reg_name == "x86AppPath":
                    browser_path = reg_value
            except WindowsError as _:
                pass
    except WindowsError as _:
        pass
    finally:
        # Closing iexplorer_main_key
        _winreg.CloseKey(iexplorer_main_key)

    # Updating "found browser" list
    found_browsers.append(["explorer", "Internet Explorer", browser_version, browser_path])

    ###########################
    # SECTION: MICROSOFT EDGE #
    ###########################

    # Searching for Microsoft Edge only in Windows 10 or later
    if int(windows_release) >= 10:
        try:
            # Opening packages key (contains a key for Microsoft Edge)
            packages_key = _winreg.OpenKey(_winreg.HKEY_CURRENT_USER, utils.PACKAGES_KEY, 0, _winreg.KEY_READ)
            # Searching in sub keys of packages key for Microsoft Edge
            for s_k in range(_winreg.QueryInfoKey(packages_key)[0]):
                # Sub key name
                sub_key_name = _winreg.EnumKey(packages_key, s_k)
                # Microsoft Edge matches a sub key name
                if "MicrosoftEdge" in sub_key_name:
                    # Matching Microsoft Edge key name
                    edge_key_name = "\\".join([utils.PACKAGES_KEY, sub_key_name])
                    try:
                        # Opening matching Microsoft Edge key
                        edge_key = _winreg.OpenKey(_winreg.HKEY_CURRENT_USER, edge_key_name, 0, _winreg.KEY_READ)
                        # Searching in edge_key values for version and installation path
                        for val in range(_winreg.QueryInfoKey(edge_key)[1]):
                            try:
                                # edge_key values
                                reg_name, reg_value, reg_type = _winreg.EnumValue(edge_key, val)
                                # Microsoft Edge version value
                                if reg_name == "PackageID":
                                    browser_version = reg_value
                                # Microsoft Edge installation path
                                if reg_name == "PackageRootFolder":
                                    browser_path = reg_value
                            except WindowsError as _:
                                pass
                    except WindowsError as _:
                        pass
                    finally:
                        # Closing edge_key
                        _winreg.CloseKey(edge_key)
        except WindowsError as _:
            pass
        finally:
            # Closing packages_key
            _winreg.CloseKey(packages_key)

        # Updating "found browser" list
        found_browsers.append(["edge", "Microsoft Edge", browser_version.split("_")[1], browser_path])

    # Returning results list with all found browsers values
    return found_browsers
