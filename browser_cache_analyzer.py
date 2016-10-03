# -*- coding: utf-8 -*-
# !/usr/bin/env python

# PyQt4 imports
from PyQt4 import QtGui, QtCore

# Python imports
import platform
import os

# Project imports
from gui import python_converted_gui
from operating_systems import windows
from utilities import utils


class BrowserCacheAnalyzer(QtGui.QMainWindow, python_converted_gui.Ui_AnalyzerMainWindow):

    def __init__(self, parent=None):
        super(BrowserCacheAnalyzer, self).__init__(parent)

        # Setting up the application user interface from python converted gui
        self.setupUi(self)

    ##########################################
    # SECTION: APPLICATION ELEMENTS SETTINGS #
    ##########################################

        # "System info" group box elements
        self.line_system_os_name.setStyleSheet("* {background-color: transparent; }")
        self.line_system_os_name.setReadOnly(True)
        self.line_system_os_name.setFrame(False)
        self.line_system_release.setStyleSheet("* {background-color: transparent; }")
        self.line_system_release.setReadOnly(True)
        self.line_system_release.setFrame(False)
        self.line_system_release_version.setStyleSheet("* {background-color: transparent; }")
        self.line_system_release_version.setReadOnly(True)
        self.line_system_release_version.setFrame(False)
        self.line_system_hostname.setStyleSheet("* {background-color: transparent; }")
        self.line_system_hostname.setReadOnly(True)
        self.line_system_hostname.setFrame(False)

        # "Selected browser" group box elements
        self.line_browser_selected.setStyleSheet("* {background-color: transparent; }")
        self.line_browser_selected.setReadOnly(True)
        self.line_browser_selected.setFrame(False)
        self.line_browser_version.setStyleSheet("* {background-color: transparent; }")
        self.line_browser_version.setReadOnly(True)
        self.line_browser_version.setFrame(False)
        self.line_browser_install_path.setStyleSheet("* {background-color: transparent; }")
        self.line_browser_install_path.setReadOnly(True)
        self.line_browser_install_path.setFrame(False)
        self.line_browser_default_cache_path.setStyleSheet("* {background-color: transparent; }")
        self.line_browser_default_cache_path.setReadOnly(True)
        self.line_browser_default_cache_path.setFrame(False)

        # "Table found browsers"
        self.table_found_browsers.setColumnCount(4)
        self.table_found_browsers.setAlternatingRowColors(True)
        self.table_found_browsers.setColumnWidth(0, len("Icon") + 50)
        self.table_found_browsers.setHorizontalHeaderLabels(['', 'Browser Name', 'Version', 'Installation Path'])
        self.table_found_browsers.horizontalHeader().setResizeMode(1, QtGui.QHeaderView.Stretch)
        self.table_found_browsers.horizontalHeader().setResizeMode(3, QtGui.QHeaderView.Stretch)
        self.table_found_browsers.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.table_found_browsers.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
        self.table_found_browsers.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.table_found_browsers.setToolTip("Click on a row to select a browser")

    #######################
    # SECTION: ATTRIBUTES #
    #######################

        # Mouse cursor coordinates on left click over the application window
        self.mouse_press_position = None

        # List of found browsers in the system
        self.found_browsers_list = None

        # Selection from "table found browsers"
        self.found_browsers_table_selection = None

        # Matching browser key in "browsers default cache paths dictionary" (e.g "chrome" for "Google Chrome")
        self.matching_browser_key = None

        # Default cache path for selected browser
        self.default_cache_path = None

    ##########################################
    # SECTION: SIGNALS AND SLOTS CONNECTIONS #
    ##########################################

        # Application "minimize" and "close" buttons
        self.button_application_minimize.clicked.connect(self.showMinimized)
        self.button_application_close.clicked.connect(self.close_application)

        # Other application elements
        self.button_welcome_screen_next.clicked.connect(self.set_browser_choice_screen)
        self.table_found_browsers.itemClicked.connect(self.enable_button_browser_choice_screen_next)
        self.button_browser_choice_screen_next.clicked.connect(self.set_folder_choice_screen)

    ###########################
    # SECTION: WELCOME SCREEN #
    ###########################

        # Setting "welcome screen" as application start screen
        self.stackedWidget.setCurrentIndex(0)

        # If "welcome screen", "system info" and "selected browser info" group boxes are not visible
        if self.stackedWidget.currentIndex() == 0:
            self.groupBox_system_info.setVisible(False)
            self.groupBox_selected_browser_info.setVisible(False)

    ##################################
    # SECTION: BROWSER CHOICE SCREEN #
    ##################################

    def set_browser_choice_screen(self):
        """
        Slot for "next" button in "welcome screen".
        Setting "browser choice screen": stacked widget index = 1, visible "system info" group box with system values,
        not visible "selected browser" group box and "table found browsers" containing found browsers in the system.
        :return:
        """

        # Setting "browser choice screen"
        self.stackedWidget.setCurrentIndex(1)

        # "System info" group box visible
        self.groupBox_system_info.setVisible(True)

        # "Next" button not enabled (No item selected from "table found browsers")
        self.button_browser_choice_screen_next.setEnabled(False)

        # "System info" values
        self.line_system_os_name.setText(platform.system())
        self.line_system_release.setText(platform.release())
        self.line_system_release_version.setText(platform.version())
        self.line_system_hostname.setText(platform.node())

        # Searching browsers in the system (depending on OS)
        # Microsoft Windows
        if "windows" in platform.system().lower():
            self.found_browsers_list = windows.finder.browsers_finder(platform.release())
        # Other OSs
        # else:
            # Code for other OSs #

        # "Table found browsers"
        for idx, brw in enumerate(self.found_browsers_list):
            # Inserting a new row for each browser in "found browsers list"
            self.table_found_browsers.insertRow(idx)
            # Browser name (e.g "chrome" for Google Chrome) to match the right browser icon
            browser_name = brw[0]
            # Column 0 (browser icon)
            self.table_found_browsers.setCellWidget(idx, 0, BrowserIconWidget(icon_name=browser_name))
            # Columns 1, 2, 3 (found browser info)
            self.table_found_browsers.setItem(idx, 1, QtGui.QTableWidgetItem(brw[1]))
            self.table_found_browsers.setItem(idx, 2, QtGui.QTableWidgetItem(brw[2]))
            self.table_found_browsers.setItem(idx, 3, QtGui.QTableWidgetItem(brw[3]))

    def enable_button_browser_choice_screen_next(self):
        """
        Slot for "table found browsers".
        Enabling "next" button on "browser choice screen" if an item from "table found browser" is selected.
        :return:
        """

        # Selection from "table found browsers"
        self.found_browsers_table_selection = self.table_found_browsers.selectedItems()

        # If selection, enabling "next" button
        if self.found_browsers_table_selection:
            self.button_browser_choice_screen_next.setEnabled(True)

    #################################
    # SECTION: FOLDER CHOICE SCREEN #
    #################################

    def set_folder_choice_screen(self):
        """
        Slot for "next" button in "browser choice screen".
        Setting "folder choice screen": stacked widget index = 2 and visible "selected browser info" group box
        with browser values.
        Checking if selected cache path is valid for selected browser and analyzing it.
        :return:
        """

        # Setting "folder choice screen"
        self.stackedWidget.setCurrentIndex(2)

        # "Selected browser" group box visible
        self.groupBox_selected_browser_info.setVisible(True)

        # Values for selected browser from "table found browsers" selection
        browser_name = self.found_browsers_table_selection[0].text()
        browser_version = self.found_browsers_table_selection[1].text()
        browser_install_path = self.found_browsers_table_selection[2].text()

        # Default cache paths for supported browsers
        for k in utils.BROWSERS_DEFAULT_CACHE_PATHS.keys():
            # A key in dictionary matches browser name
            if k[0] in str(browser_name).lower():
                self.matching_browser_key = k[0]
                # Retrieving default path in dictionary
                self.default_cache_path = utils.BROWSERS_DEFAULT_CACHE_PATHS.get(
                    (self.matching_browser_key, platform.system().lower(), platform.release()),
                    "Missing default cache path for selected browser")

        # "Selected browser" values
        self.line_browser_selected.setText(browser_name)
        self.line_browser_version.setText(browser_version)
        self.line_browser_install_path.setText(browser_install_path)
        self.line_browser_install_path.home(False)
        self.line_browser_default_cache_path.setText(self.default_cache_path)
        self.line_browser_default_cache_path.home(False)

        # "Selected browser" icon
        icon_path = os.path.join(utils.ICONS_PATH, "{icon}.png".format(icon=self.matching_browser_key))
        browser_icon = QtGui.QPixmap(icon_path)
        self.label_browser_icon.setPixmap(browser_icon)

        # Checking if default cache path for selected browser is valid
        default_path_is_valid = utils.check_valid_cache_path(self.matching_browser_key, self.default_cache_path)

        # Mark path for valid default cache path
        if default_path_is_valid:
            # Valid mark path
            mark_path = os.path.join(utils.ICONS_PATH, "mark_valid.png")
            self.label_browser_valid_path_mark.setToolTip("Path is valid for selected browser")
        # Mark path for not valid default cache path
        else:
            # Not valid mark path
            mark_path = os.path.join(utils.ICONS_PATH, "mark_not_valid.png")
            self.label_browser_valid_path_mark.setToolTip("Path is not valid for selected browser")

        # Setting mark
        mark_icon = QtGui.QPixmap(mark_path)
        self.label_browser_valid_path_mark.setPixmap(mark_icon)

    ##############################
    # SECTION: CLOSE APPLICATION #
    ##############################

    def close_application(self):
        """
        Slot for application "close" button.
        A message box will ask to confirm before quitting.
        :return:
        """

        # Confirmation before quitting
        msg_confirm_exit = QtGui.QMessageBox.question(QtGui.QMessageBox(), "Confirm",
                                                      "Are you sure you want to quit?",
                                                      QtGui.QMessageBox.Yes | QtGui.QMessageBox.No,
                                                      QtGui.QMessageBox.No)

        # If "yes" button clicked, quitting application
        if msg_confirm_exit == QtGui.QMessageBox.Yes:
            self.close()

    ######################################################################
    # SECTION: MOUSE METHODS OVERRIDE (Application window drag and drop) #
    ######################################################################

    def mousePressEvent(self, event):
        """
        Override for QtGui.QWidget.mousePressEvent to calculate mouse position at click.
        Event position is relative to the application window.
        :param event: QtGui.QMouseEvent
        :return:
        """

        # Mouse cursor coordinates relative to the application window
        self.mouse_press_position = event.pos()

    def mouseMoveEvent(self, event):
        """
        Override for QtGui.QWidget.mouseMoveEvent to drag the application window.
        Event buttons indicates the button state when the event was generated.
        Event position is the global position of the mouse cursor at the time of the event.
        :param event: QtGui.QMouseEvent
        :return:
        """

        # Application window move (with mouse left button)
        if event.buttons() == QtCore.Qt.LeftButton:
            self.move(event.globalPos() - self.mouse_press_position)

    ###########################################################################
    # SECTION: BROWSER ICON WIDGET (Browsers icons in "table found browsers") #
    ###########################################################################


class BrowserIconWidget(QtGui.QLabel):
    """
    Selection for browser icon in "table found browsers".
    Setting a Browser Icon Widget for the first column of "table found browsers", selecting the right icon according
    to the browser name.
    :param icon_name: browser name from "found browser list"
    """

    def __init__(self, parent=None, icon_name=None):
        super(BrowserIconWidget, self).__init__(parent)

        # Center alignment
        self.setAlignment(QtCore.Qt.AlignCenter)

        # Setting browser icon
        icon_path = os.path.join(utils.ICONS_PATH, "{name}.png".format(name=icon_name))
        browser_icon = QtGui.QPixmap(icon_path)
        self.setPixmap(browser_icon)
