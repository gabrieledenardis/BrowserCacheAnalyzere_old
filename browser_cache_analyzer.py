# -*- coding: utf-8 -*-
# !/usr/bin/env python

# PyQt4 imports
from PyQt4 import QtGui, QtCore

# Python imports
import platform
import os
import datetime

# Project imports
from gui import python_converted_gui
from gui import python_converted_dialog_chrome
from operating_systems import windows
from utilities import utils
from browsers import chrome


class BrowserCacheAnalyzer(QtGui.QMainWindow, python_converted_gui.Ui_AnalyzerMainWindow):

    def __init__(self, parent=None):
        super(BrowserCacheAnalyzer, self).__init__(parent)

        # Setting up the application user interface from python converted gui
        self.setupUi(self)

##########################################
# SECTION: APPLICATION ELEMENTS SETTINGS #
##########################################

        # "System info" group box elements
        self.groupBox_system_info.setStyleSheet("QLineEdit { background-color: transparent }")
        for item in self.groupBox_system_info.findChildren(QtGui.QLineEdit):
            item.setReadOnly(True)
            item.setFrame(False)

        # "Selected browser" group box elements
        self.groupBox_selected_browser_info.setStyleSheet("QLineEdit { background-color: transparent }")
        for item in self.groupBox_selected_browser_info.findChildren(QtGui.QLineEdit):
            item.setReadOnly(True)
            item.setFrame(False)

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

        # "Folder choice screen" folder info elements
        self.line_analysis_input_path.setStyleSheet("background-color: transparent")
        self.line_analysis_input_path.setReadOnly(True)

        # Setting text for all results label in "Analysis folder" groupBox selectable by mouse
        for label in self.groupBox_analysis_input_folder.findChildren(QtGui.QLabel):
            if "label_folder" in label.objectName() or "label_file" in label.objectName():
                label.setTextInteractionFlags(QtCore.Qt.TextSelectableByMouse)

        # "Folder choice screen" list folder
        self.list_input_folder.setToolTip("Select a file to show info")

        # "Folder preview" groupBox
        self.groupBox_input_folder_preview.setStyleSheet("QLabel { color: rgb(70, 70, 70) }")
        for label in self.groupBox_input_folder_preview.findChildren(QtGui.QLabel):
            if "label_file" in label.objectName():
                label.clear()

        # "Table analysis results"
        self.table_analysis_results.setColumnCount(4)
        self.table_analysis_results.setAlternatingRowColors(True)
        self.table_analysis_results.setHorizontalHeaderLabels(['Key hash', 'Key URL', 'Content Type',
                                                               'Creation Time'])
        self.table_analysis_results.horizontalHeader().setResizeMode(QtGui.QHeaderView.Stretch)
        self.table_analysis_results.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.table_analysis_results.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
        self.table_analysis_results.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.table_analysis_results.setToolTip("Right click for options")
        self.table_analysis_results.setSortingEnabled(True)
        self.table_analysis_results.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)

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

        # Current selected path to analyze
        self.current_input_path = None

        # Analyzer thread for "Google chrome"
        self.chrome_analyzer_thread = None

        # List containing analysis results
        self.analysis_results_list = []

        # QDialog for advanced info for "chrome" results
        self.dialog_results_chrome = None

        # Clipboard to store copied values
        self.clipboard = None

##########################################
# SECTION: SIGNALS AND SLOTS CONNECTIONS #
##########################################

        # Application "minimize" and "close" buttons
        self.button_application_minimize.clicked.connect(self.showMinimized)
        self.button_application_close.clicked.connect(self.close_application)

        # Other application elements
        self.button_next_welcome_screen.clicked.connect(self.set_browser_choice_screen)
        self.table_found_browsers.itemClicked.connect(self.enable_button_next_browser_choice_screen)
        self.button_next_browser_choice_screen.clicked.connect(self.set_input_folder_screen)
        self.button_back_input_folder_screen.clicked.connect(self.set_browser_choice_screen)
        self.button_analyze_default_path.clicked.connect(self.select_input_cache_folder)
        self.button_analyze_other_path.clicked.connect(self.select_input_cache_folder)
        self.list_input_folder.itemClicked.connect(self.file_info)
        self.button_confirm_analysis.clicked.connect(self.set_analysis_screen)
        self.button_stop_analysis.clicked.connect(self.stop_analysis)
        self.button_back_analysis_screen.clicked.connect(self.set_input_folder_screen)
        self.table_analysis_results.customContextMenuRequested.connect(self.table_results_context_menu)

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
        :return: nothing
        """

        # Setting "browser choice screen"
        self.stackedWidget.setCurrentIndex(1)

        # "System info" group box visible
        self.groupBox_system_info.setVisible(True)

        # "Next" button not enabled (No item selected from "table found browsers")
        self.button_next_browser_choice_screen.setEnabled(False)

        # Cleaning "table found browsers" (if back from "folder choice screen")
        self.table_found_browsers.setRowCount(0)

        # "Selected browser info" groupBox not visible (if back from "folder choice screen")
        self.groupBox_selected_browser_info.setVisible(False)

        # Getting values for system info and installed browsers in the system
        self.get_system_info()
        self.get_installed_browser()

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

    def get_system_info(self):
        """
        Getting system info and setting values in "System info" groupBox.
        :return: nothing
        """

        # "System info" values
        self.line_system_os_name.setText(platform.system())
        self.line_system_release.setText(platform.release())
        self.line_system_release_version.setText(platform.version())
        self.line_system_hostname.setText(platform.node())

    def get_installed_browser(self):
        """
        Searching for installed browsers in the system.
        :return: nothing
        """

        # Searching browsers in the system (depending on OS)
        # Microsoft Windows
        if "windows" in platform.system().lower():
            self.found_browsers_list = windows.finder.browsers_finder(platform.release())
        # TODO: Code for other OSs

    def enable_button_next_browser_choice_screen(self):
        """
        Slot for "table found browsers".
        Enabling "next" button on "browser choice screen" if an item from "table found browser" is selected.
        :return: nothing
        """

        # Selection from "table found browsers"
        self.found_browsers_table_selection = self.table_found_browsers.selectedItems()

        # If selection, enabling "next" button
        if self.found_browsers_table_selection:
            self.button_next_browser_choice_screen.setEnabled(True)

######################################
# SECTION: INPUT CACHE FOLDER SCREEN #
######################################

    def set_input_folder_screen(self):
        """
        Slot for "next" button in "browser choice screen" and for "back" button in "analysis screen".
        If "next" button in "browser choice screen" clicked, stacked widget index = 2, visible "selected browser info"
        groupBox with selected browser values and cleaning info for selected input folder (if "input folder screen"
        already visited earlier.
        If "back" button in "analysis screen" clicked, stacked widget index = 2 or asking to stop running analysis if
        is running and setting stacked widget index = 2.
        :return: nothing
        """

        # Detecting clicked button ("default" or "other path")
        clicked_button = self.sender().objectName()

        # "Default" path button
        if clicked_button == "button_next_browser_choice_screen":
            # Setting current "stacked widget" index to "input folder selection screen"
            self.stackedWidget.setCurrentIndex(2)

            # Visible "selected browser info" groupBox
            self.groupBox_selected_browser_info.setVisible(True)

            # Info for selected browser
            self.get_selected_browser_info()

            # Selection for input cache folder to analyze
            self.select_input_cache_folder()

            # "Confirm analysis button" not enabled (yet no input folder selected)
            self.button_confirm_analysis.setEnabled(False)

            # If "input folder selection screen" already visited earlier, cleaning values in "analysis input groupBox"
            # and in "input folder preview groupBox"
            for item in self.groupBox_analysis_input_folder.findChildren((QtGui.QLabel, QtGui.QLineEdit)):
                if "label_folder_" in item.objectName():
                    item.clear()
                if "line_analysis_input_path" in item.objectName():
                    item.clear()

            for item in self.groupBox_input_folder_preview.findChildren((QtGui.QLabel, QtGui.QListWidget)):
                if "label_file_" in item.objectName():
                    item.clear()
                if "list_input_folder" in item.objectName():
                    item.clear()

        elif clicked_button == "button_back_analysis_screen":

            # Button "stop analysis" enabled (Analysis is still running)
            if self.button_stop_analysis.isEnabled():

                browser_name = self.found_browsers_table_selection[0].text()

                # Confirmation quitting running analysis
                msg_analysis_running = QtGui.QMessageBox.question(QtGui.QMessageBox(), "Analysis running",
                                                                  "Analysis for {browser} is still running. Stop?"
                                                                  .format(browser=browser_name),
                                                                  QtGui.QMessageBox.Yes | QtGui.QMessageBox.No,
                                                                  QtGui.QMessageBox.No)

                # If "yes" button clicked, quitting analysis
                if msg_analysis_running == QtGui.QMessageBox.Yes:
                    # Stopping analysis
                    self.stop_analysis()
                    # Setting current "stacked widget" index to "input folder selection screen"
                    self.stackedWidget.setCurrentIndex(2)
            # Analysis stopped
            else:
                self.stackedWidget.setCurrentIndex(2)

    def get_selected_browser_info(self):
        """
        Slot for "next" button in "browser choice screen".
        Retrieving info for selected browser.
        Checking if selected cache path is valid for selected browser and analyzing it.
        :return: nothing
        """

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

            # Enabling "analyze default path" button if default path is not valid
            self.button_analyze_default_path.setEnabled(True)
        # Mark path for not valid default cache path
        else:
            # Not valid mark path
            mark_path = os.path.join(utils.ICONS_PATH, "mark_not_valid.png")
            self.label_browser_valid_path_mark.setToolTip("Path is not valid for selected browser")

        # Setting mark
        mark_icon = QtGui.QPixmap(mark_path)
        self.label_browser_valid_path_mark.setPixmap(mark_icon)

    def select_input_cache_folder(self):
        """
        Slot for "button analyze default path" and for "button analyze other path".
        A path to analyze will be chosen and checked to be valid for selected browser.
        :return: nothing
        """

        # Detecting clicked button ("default" or "other path")
        clicked_button = self.sender().objectName()

        # "Default" path button
        if clicked_button == "button_analyze_default_path":
            # Setting "current input path" as "default path"
            self.current_input_path = self.default_cache_path

            # Displaying selected input path (default path)
            self.line_analysis_input_path.setText(self.current_input_path)
            self.line_analysis_input_path.home(False)
        # "Other path" button
        elif clicked_button == "button_analyze_other_path":
            # Selecting an input path to analyze
            dialog_input_path = QtGui.QFileDialog().getExistingDirectory(self, "Select a cache folder to analyze",
                                                                         os.path.join("C:", os.sep, "Users",
                                                                                      unicode(os.environ['USERNAME']),
                                                                                      "Desktop"),
                                                                         QtGui.QFileDialog.DontUseNativeDialog |
                                                                         QtGui.QFileDialog.ShowDirsOnly |
                                                                         QtGui.QFileDialog.ReadOnly)

            # Convert QString from QDialog to unicode
            dialog_input_path = unicode(dialog_input_path)

            # Checking if selected path is valid for selected browser
            other_path_is_valid = utils.check_valid_cache_path(self.matching_browser_key, dialog_input_path)

            # Selected path to analyze is correct
            if other_path_is_valid:
                # Setting "current input path" as selected path from QDialog
                self.current_input_path = dialog_input_path

                self.line_analysis_input_path.setText(self.current_input_path.replace("/", "\\"))
                self.line_analysis_input_path.home(False)
            # Selected path to analyze is not correct
            else:
                # Path is selected but not correct
                if dialog_input_path:
                    browser = self.found_browsers_table_selection[0].text()

                    QtGui.QMessageBox.warning(QtGui.QMessageBox(), "Wrong input path",
                                              "{path} <br> is not correct for {browser}"
                                              .format(path=dialog_input_path, browser=browser),
                                              QtGui.QMessageBox.Yes)
                # No selected path to analyze
                else:
                    QtGui.QMessageBox.information(QtGui.QMessageBox(), "No selected path",
                                                  "Seems you did not select an input folder. <br> Please selected one",
                                                  QtGui.QMessageBox.Yes)

        if self.current_input_path:
            # Selected folder dimension
            folder_dimension = 0
            for dir_path, dir_names, file_names in os.walk(self.current_input_path):
                for f in file_names:
                    fp = os.path.join(dir_path, f)
                    folder_dimension += os.path.getsize(fp)

            # Other folder info
            folder_num_elements = len(os.listdir(self.current_input_path))
            folder_creation_time = os.stat(self.current_input_path).st_ctime
            folder_last_access_time = os.stat(self.current_input_path).st_atime
            readable_creation_time = datetime.datetime.fromtimestamp(folder_creation_time) \
                .strftime("%A - %d %B %Y - %H:%M:%S")
            readable_last_access_time = datetime.datetime.fromtimestamp(folder_last_access_time) \
                .strftime("%A - %d %B %Y - %H:%M:%S")

            # Folder info labels text
            self.label_folder_dimension.setText(str(folder_dimension))
            self.label_folder_num_elements.setText(str(folder_num_elements))
            self.label_folder_creation_time.setText(str(readable_creation_time))
            self.label_folder_last_access.setText(str(readable_last_access_time))

            # "List input folder"
            self.list_input_folder.clear()
            self.list_input_folder.addItems(os.listdir(self.current_input_path))

            if self.current_input_path:
                self.button_confirm_analysis.setEnabled(True)

    def file_info(self):
        """
        Slot for "list input widget" in "folder choice screen".
        Calculating info about selected file from the list widget.
        :return: nothing
        """

        # Selected item from "list input folder" list widget
        selected_item = unicode(self.list_input_folder.selectedItems()[0].text())
        file_path = os.path.join(self.current_input_path, selected_item)

        # Selected file hashing
        md5 = utils.file_cryptography(file_path=file_path)['md5']
        sha1 = utils.file_cryptography(file_path=file_path)['sha1']

        # Other file info
        file_size = os.stat(file_path).st_size
        creation_time = os.stat(file_path).st_ctime
        last_modified_time = os.stat(file_path).st_mtime
        last_access_time = os.stat(file_path).st_atime

        # Selected file info
        creation_time_readable = datetime.datetime.fromtimestamp(creation_time).strftime("%A - %d %B %Y - %H:%M:%S")
        last_modified_time_readable = datetime.datetime.fromtimestamp(last_modified_time) \
            .strftime("%A - %d %B %Y - %H:%M:%S")
        last_access_time_readable = datetime.datetime.fromtimestamp(last_access_time) \
            .strftime("%A - %d %B %Y - %H:%M:%S")

        # File info labels text
        self.label_file_selected.setText(selected_item)
        self.label_file_dimension.setText(str(file_size))
        self.label_file_creation_time.setText(str(creation_time_readable))
        self.label_file_last_modified.setText(str(last_modified_time_readable))
        self.label_file_last_access.setText(str(last_access_time_readable))
        self.label_file_md5.setText(str(md5))
        self.label_file_sha1.setText(str(sha1))

############################
# SECTION: ANALYSIS SCREEN #
############################

    def set_analysis_screen(self):
        """
        Slot for "confirm and start analysis" button in "folder choice screen".
        Setting "analysis screen": stacked widget index = 3.
        :return:
        """
        # Setting "analysis screen"
        self.stackedWidget.setCurrentIndex(3)

        # Clipboard to store copied values from "table analysis results"
        self.clipboard = QtGui.QApplication.clipboard()

        # Rows for "table analysis results" = 0 (if "analysis screen" already visited earlier)
        self.table_analysis_results.setRowCount(0)

        self.analysis_results_list = []

        # "Chrome analyzer thread"
        self.chrome_analyzer_thread = chrome.chrome_analyzer.ChromeAnalyzerThread(input_path=self.current_input_path)
        self.chrome_analyzer_thread.update_results_table_signal.connect(self.analysis_table_update)
        self.chrome_analyzer_thread.finished.connect(self.analysis_terminated)
        self.chrome_analyzer_thread.start()

    def analysis_table_update(self, num_elem, key_hash, key_data, content_type, creation_time):
        """
        Slot for "update results table" signal from "chrome analyzer thread".
        :param num_elem: position of the element in list of found cache entry instances.
        :param key_hash: hash of the key in found cache entry.
        :param key_data: data in cache entry.
        :param content_type: content type for the data in cache entry.
        :param creation_time: cache entry creation time.
        :return: nothing
        """

        # If analysis is running, enabling "stop" analysis button
        self.button_stop_analysis.setEnabled(True)

        # Insert cache entry values in "table analysis results"
        self.table_analysis_results.insertRow(num_elem)
        self.table_analysis_results.setItem(num_elem, 0, QtGui.QTableWidgetItem(key_hash))
        self.table_analysis_results.setItem(num_elem, 1, QtGui.QTableWidgetItem(key_data))
        self.table_analysis_results.setItem(num_elem, 2, QtGui.QTableWidgetItem(content_type))
        self.table_analysis_results.setItem(num_elem, 3, QtGui.QTableWidgetItem(creation_time))
        self.table_analysis_results.scrollToBottom()

        # Copying "cache entries list" from "chrome analyzer thread" to avoid rescan for html export (if any).
        self.analysis_results_list = self.chrome_analyzer_thread.cache_entries_list[:]

    def stop_analysis(self):
        """
        Slot for "stop analysis" button.
        Setting stop signal for "ChromeAnalyzerThread" to stop cache analysis.
        :return: nothing
        """

        # Setting stop signal
        self.chrome_analyzer_thread.stop_signal.set()

        browser_name = self.found_browsers_table_selection[0].text()

        QtGui.QMessageBox.warning(QtGui.QMessageBox(), "Analysis stopped",
                                  "Analysis for {browser} stopped by user".format(browser=browser_name),
                                  QtGui.QMessageBox.Ok)

    def analysis_terminated(self):
        """
        Slot for "finished signal" from "chrome analyzer thread".
        :return: nothing
        """

        # Disabling "stop analysis" button and deleting "chrome analyzer thread"
        self.button_stop_analysis.setEnabled(False)
        del self.chrome_analyzer_thread

    def table_results_context_menu(self, position):
        """
        Slot for mouse right click on "table analysis results" to open a context menu for advanced results.
        :return: nothing
        """
        menu = QtGui.QMenu()
        copy_to_clipboard_action = menu.addAction("Copy item to clipboard")
        advanced_results_action = menu.addAction("Show advanced results")
        action = menu.exec_(self.table_analysis_results.mapToGlobal(position))

        if action == advanced_results_action:
            current_table_row = self.table_analysis_results.currentRow()
            current_result_item = self.analysis_results_list[current_table_row]
            self.dialog_results_chrome = ChromeCustomDialog()

            self.dialog_results_chrome.line_res_key_data.setStyleSheet("background-color: transparent")
            self.dialog_results_chrome.line_res_key_data.setFrame(False)
            self.dialog_results_chrome.line_res_key_data.setReadOnly(True)

            self.dialog_results_chrome.label_dialog_title.setText(str(current_result_item.key_hash))
            self.dialog_results_chrome.label_res_key_hash.setText(str(current_result_item.key_hash))
            self.dialog_results_chrome.label_res_next_entry_address.setText(str(current_result_item.next_entry_address))
            self.dialog_results_chrome.label_res_rank_node_address. \
                setText(str(current_result_item.rankings_node_address))
            self.dialog_results_chrome.label_res_reuse_count.setText(str(current_result_item.reuse_count))
            self.dialog_results_chrome.label_res_refetch_count.setText(str(current_result_item.refetch_count))
            self.dialog_results_chrome.label_res_entry_state.setText(str(current_result_item.entry_state))
            self.dialog_results_chrome.label_res_creation_time.setText(str(current_result_item.creation_time))
            self.dialog_results_chrome.label_res_key_data_size.setText(str(current_result_item.key_data_size))
            self.dialog_results_chrome.label_res_long_key_address. \
                setText(str(current_result_item.long_key_data_address))
            self.dialog_results_chrome.label_res_cache_entry_flags.setText(str(current_result_item.cache_entry_flags))
            self.dialog_results_chrome.line_res_key_data.setText(str(current_result_item.key_data))
            self.dialog_results_chrome.line_res_key_data.home(False)

            # "Chrome advanced info" QDialog settings
            for label in self.dialog_results_chrome.findChildren(QtGui.QLabel):
                if "label_res" in label.objectName():
                    label.setTextInteractionFlags(QtCore.Qt.TextSelectableByMouse)

            self.dialog_results_chrome.exec_()

        if action == copy_to_clipboard_action:
            selection = self.table_analysis_results.currentItem().text()
            self.clipboard.clear()
            self.clipboard.setText(selection)
            QtGui.QMessageBox.information(QtGui.QMessageBox(), "Clipboard",
                                          "{selection}\nElement copied to clipboard".format(selection=selection),
                                          QtGui.QMessageBox.Ok)

    ##############################
    # SECTION: CLOSE APPLICATION #
    ##############################

    def close_application(self):
        """
        Slot for application "close" button.
        A message box will ask to confirm before quitting.
        :return: nothing
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
        :return: nothing
        """

        # Mouse cursor coordinates relative to the application window
        self.mouse_press_position = event.pos()

    def mouseMoveEvent(self, event):
        """
        Override for QtGui.QWidget.mouseMoveEvent to drag the application window.
        Event buttons indicates the button state when the event was generated.
        Event position is the global position of the mouse cursor at the time of the event.
        :param event: QtGui.QMouseEvent
        :return: nothing
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


class ChromeCustomDialog(QtGui.QDialog, python_converted_dialog_chrome.Ui_DialogResultsChrome):

    def __init__(self, parent=None):
        super(ChromeCustomDialog, self).__init__(parent)

        # Setting up the application user interface from python converted gui
        self.setupUi(self)

        # Stylesheet for QDialog background color
        self.setStyleSheet(" background-color : lightgray")

        # Mouse cursor coordinates on left click over the application window
        self.mouse_press_position = None

        # Flag for frameless QDialog
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)

        # Closing QDialog on "button close" click
        self.button_dialog_close.clicked.connect(self.close)

    def mousePressEvent(self, event):
        """
        Override for QtGui.QWidget.mousePressEvent to calculate mouse position at click.
        Event position is relative to the application window.
        :param event: QtGui.QMouseEvent
        :return: nothing
        """

        # Mouse cursor coordinates relative to the application window
        self.mouse_press_position = event.pos()

    def mouseMoveEvent(self, event):
        """
        Override for QtGui.QWidget.mouseMoveEvent to drag the application window.
        Event buttons indicates the button state when the event was generated.
        Event position is the global position of the mouse cursor at the time of the event.
        :param event: QtGui.QMouseEvent
        :return: nothing
        """

        # Application window move (with mouse left button)
        if event.buttons() == QtCore.Qt.LeftButton:
            self.move(event.globalPos() - self.mouse_press_position)
