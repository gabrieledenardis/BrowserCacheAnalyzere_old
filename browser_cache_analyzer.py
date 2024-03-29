# -*- coding: utf-8 -*-
# !/usr/bin/env python

# PyQt4 imports
from PyQt4 import QtGui, QtCore

# Python imports
import platform
import datetime
import os
import math


# Project imports
from gui import python_converted_dialog_chrome
from operating_systems import windows
from gui import python_converted_gui
from browsers import chrome
from utilities import utils


class BrowserCacheAnalyzer(QtGui.QMainWindow, python_converted_gui.Ui_AnalyzerMainWindow):

    def __init__(self, parent=None):
        super(BrowserCacheAnalyzer, self).__init__(parent)

        # Setting up the application user interface from python converted gui
        self.setupUi(self)

        # Frameless window
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)

##########################################
# SECTION: APPLICATION ELEMENTS SETTINGS #
##########################################

        # "System info" groupBox
        self.groupBox_system_info.setStyleSheet("QLineEdit { background-color: transparent }")
        self.groupBox_system_info.setFocusPolicy(QtCore.Qt.ClickFocus)
        for line in self.groupBox_system_info.findChildren(QtGui.QLineEdit):
            line.installEventFilter(self)
            line.setReadOnly(True)
            line.setFrame(False)

        # "Selected browser" groupBox
        self.groupBox_selected_browser_info.setStyleSheet("QLineEdit { background-color: transparent }")
        self.groupBox_selected_browser_info.setFocusPolicy(QtCore.Qt.ClickFocus)
        for line in self.groupBox_selected_browser_info.findChildren(QtGui.QLineEdit):
            line.installEventFilter(self)
            line.setReadOnly(True)
            line.setFrame(False)

        # "Found browsers" groupBox
        self.groupBox_found_browsers.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.groupBox_found_browsers.installEventFilter(self)

        # "Table found browsers"
        self.table_found_browsers.setColumnCount(4)
        self.table_found_browsers.setHorizontalHeaderLabels(['', 'Browser Name', 'Version', 'Installation Path'])
        self.table_found_browsers.horizontalHeader().setResizeMode(1, QtGui.QHeaderView.Stretch)
        self.table_found_browsers.horizontalHeader().setResizeMode(3, QtGui.QHeaderView.Stretch)
        self.table_found_browsers.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
        self.table_found_browsers.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.table_found_browsers.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.table_found_browsers.setToolTip("Click on a row to select a browser")
        self.table_found_browsers.setColumnWidth(0, len("Icon") + 50)
        self.table_found_browsers.setAlternatingRowColors(True)

        # "Analysis input folder" groupBox
        self.groupBox_analysis_input_folder.setStyleSheet("QLineEdit { background-color: transparent }")
        for line in self.groupBox_analysis_input_folder.findChildren(QtGui.QLineEdit):
            if "line_analysis_input_path" != line.objectName():
                line.setFrame(False)
            line.setFocusPolicy(QtCore.Qt.ClickFocus)
            line.installEventFilter(self)
            line.setReadOnly(True)

        # "Folder preview" groupBox
        self.groupBox_preview_input_folder.setStyleSheet("color: rgb(70, 70, 70) ")
        self.list_input_folder_preview.setToolTip("Select a file to show info")
        for line in self.groupBox_preview_input_folder.findChildren(QtGui.QLineEdit):
            line.setStyleSheet("background-color: transparent ")
            line.installEventFilter(self)
            line.setReadOnly(True)
            line.setFrame(False)

        #  "Table analysis results"
        self.table_analysis_preview.setColumnCount(4)
        self.table_analysis_preview.setHorizontalHeaderLabels(
            ['Key Hash', 'Key URL', 'Content Type', 'Creation Time']
        )
        self.table_analysis_preview.horizontalHeader().setResizeMode(QtGui.QHeaderView.Stretch)
        self.table_analysis_preview.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
        self.table_analysis_preview.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.table_analysis_preview.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.table_analysis_preview.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.table_analysis_preview.setToolTip("Right click for options")
        self.table_analysis_preview.setAlternatingRowColors(True)
        self.table_analysis_preview.setSortingEnabled(True)

        # "Analysis results" groupBox
        self.line_input_path_analysis.setStyleSheet("background-color: transparent")
        self.line_input_path_analysis.installEventFilter(self)
        self.line_input_path_analysis.setReadOnly(True)
        self.line_input_path_analysis.setFrame(False)

        # "Exporting" groupBox
        self.line_input_path_exporting.setStyleSheet("background-color: transparent")
        self.line_input_path_exporting.installEventFilter(self)
        self.line_input_path_exporting.setReadOnly(True)
        self.line_input_path_exporting.setFrame(False)

        self.line_output_path_exporting.setStyleSheet("background-color: transparent")
        self.line_output_path_exporting.installEventFilter(self)
        self.line_output_path_exporting.setReadOnly(True)
        self.line_output_path_exporting.setFrame(False)

        # Application buttons
        for item in self.findChildren(QtGui.QPushButton):
            item.setStyleSheet(
                "QPushButton {background-color: transparent; border: 1px solid darkgray}"
                "QPushButton:hover {background-color: rgb(225,225,225)}"
            )


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

        # Current selected path to analyze and current output path
        self.current_input_path = None
        self.current_output_path = None

        # Analyzer thread for "Google chrome"
        self.chrome_analyzer_thread = None
        self.chrome_export_thread = None

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
        self.button_application_close.clicked.connect(self.close_application)
        self.button_application_minimize.clicked.connect(self.showMinimized)

        # Other application elements
        self.table_analysis_preview.customContextMenuRequested.connect(self.table_results_context_menu)
        self.table_found_browsers.itemClicked.connect(self.enable_button_next_browser_choice_screen)
        self.button_back_input_folder_screen.clicked.connect(self.set_browser_choice_screen)
        self.button_next_browser_choice_screen.clicked.connect(self.set_input_folder_screen)
        self.button_next_welcome_screen.clicked.connect(self.set_browser_choice_screen)
        self.button_analyze_default_path.clicked.connect(self.select_input_cache_path)
        self.button_back_analysis_screen.clicked.connect(self.set_input_folder_screen)
        self.button_analyze_other_path.clicked.connect(self.select_input_cache_path)
        self.button_quit_analysis_screen.clicked.connect(self.close_application)
        self.button_confirm_analysis.clicked.connect(self.set_analysis_screen)
        self.button_stop_analysis_screen.clicked.connect(self.stop_analysis)
        self.button_stop_export_screen.clicked.connect(self.stop_export)
        self.list_input_folder_preview.itemClicked.connect(self.file_info)
        self.button_export_to_html.clicked.connect(self.export_to_html)


###########################
# SECTION: WELCOME SCREEN #
###########################

        # "Welcome screen" as application start screen
        self.stackedWidget.setCurrentIndex(0)

        # If "welcome screen": "system info", "selected browser info", application title and icon are not visible
        if self.stackedWidget.currentIndex() == 0:
            self.groupBox_selected_browser_info.setVisible(False)
            self.label_application_title.setVisible(False)
            self.label_application_icon.setVisible(False)
            self.groupBox_system_info.setVisible(False)


##################################
# SECTION: BROWSER CHOICE SCREEN #
##################################

    def set_browser_choice_screen(self):
        """
        Slot for "next" button in "welcome screen".
        "Browser choice screen": stacked widget index = 1, visible "system info" groupBox with system values,
        not visible "selected browser" groupBox and "table found browsers" containing found browsers in the system.
        :return: nothing
        """

        # "Browser choice screen"
        self.stackedWidget.setCurrentIndex(1)

        # "System info", application title and icon are visible
        self.label_application_title.setVisible(True)
        self.label_application_icon.setVisible(True)
        self.groupBox_system_info.setVisible(True)

        # "Next" button not enabled (no item selected from "table found browsers")
        self.button_next_browser_choice_screen.setEnabled(False)

        # If back from "folder choice screen"
        self.groupBox_selected_browser_info.setVisible(False)
        self.table_found_browsers.setRowCount(0)

        # Getting values for system info and installed browsers in the system
        self.get_system_info()
        self.get_installed_browser()

        # "Table found browsers"
        for idx, brw in enumerate(self.found_browsers_list):
            self.table_found_browsers.insertRow(idx)
            # Browser name (e.g "chrome" for Google Chrome) to match the right browser icon
            browser_name = brw[0]
            # Table columns
            self.table_found_browsers.setCellWidget(idx, 0, BrowserIconWidget(icon_name=browser_name))
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

        # Searching for browsers (depending on OS)
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

        # If an item is selected
        if self.found_browsers_table_selection:
            self.button_next_browser_choice_screen.setEnabled(True)


######################################
# SECTION: INPUT CACHE FOLDER SCREEN #
######################################

    def set_input_folder_screen(self):
        """
        Slot for "next" button in "browser choice screen" and "back" button in "analysis screen.
        "Input folder screen": stacked widget index=2 and check for open selected browser.
        Checking if selected cache path is valid for selected browser and analyzing it.
        :return: nothing
        """

        # Detecting clicked button ("next" in "browser choice screen" or "back" in "analysis results screen")
        clicked_button = self.sender().objectName()

        # "Next" button in "browser choice screen"
        if clicked_button == "button_next_browser_choice_screen":
            # Info for selected browser
            self.get_selected_browser_info()

            # If selected browser is open
            if utils.check_open_browser(browser=self.matching_browser_key):
                browser_name = self.found_browsers_table_selection[0].text()
                QtGui.QMessageBox.warning(
                    QtGui.QMessageBox(), "Open browser",
                    "{browser} seems to be open. Please close it.".format(browser=browser_name),
                    QtGui.QMessageBox.Ok
                )

            # Selected browser is not open
            else:
                self.groupBox_selected_browser_info.setVisible(True)

                # If already visited "browser choice screen"
                self.button_confirm_analysis.setEnabled(False)
                self.stackedWidget.setCurrentIndex(2)
                self.current_input_path = None

                for line in self.groupBox_analysis_input_folder.findChildren(QtGui.QLineEdit):
                    line.clear()

                for item in self.groupBox_preview_input_folder.findChildren((QtGui.QListWidget, QtGui.QLineEdit)):
                    item.clear()

                # Selection for input cache path to analyze
                self.select_input_cache_path()

        # "Back" button in "analysis screen"
        elif clicked_button == "button_back_analysis_screen":

            # If back from "analysis screen", deleting analyzer thread, resetting list of analysis results
            if self.chrome_analyzer_thread:
                del self.chrome_analyzer_thread
                self.chrome_analyzer_thread = None
                self.analysis_results_list = []


            self.stackedWidget.setCurrentIndex(2)
            self.list_input_folder_preview.clear()
            self.list_input_folder_preview.addItems(os.listdir(self.current_input_path))

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
                # Default path in dictionary
                self.default_cache_path = utils.BROWSERS_DEFAULT_CACHE_PATHS.get(
                    (self.matching_browser_key, platform.system().lower(), platform.release()),
                    "Missing default cache path for selected browser")

        # "Selected browser" values
        self.line_browser_selected.setText(browser_name)
        self.line_browser_version.setText(browser_version)
        self.line_browser_install_path.setText(browser_install_path)
        self.line_browser_default_cache_path.setText(self.default_cache_path)
        self.line_browser_default_cache_path.home(False)
        self.line_browser_install_path.home(False)

        # "Selected browser" icon
        icon_path = os.path.join(utils.ICONS_PATH, "{icon}.png".format(icon=self.matching_browser_key))
        browser_icon = QtGui.QPixmap(icon_path)
        self.label_browser_icon.setPixmap(browser_icon)

        # Checking if default cache path for selected browser is valid
        default_path_is_valid = utils.check_valid_cache_path(self.matching_browser_key, self.default_cache_path)

        # Valid default cache path
        if default_path_is_valid:
            mark_path = os.path.join(utils.ICONS_PATH, "mark_valid.png")
            self.label_browser_valid_path_mark.setToolTip("Path is valid for selected browser")
            self.button_analyze_default_path.setEnabled(True)

        # Not valid default cache path
        else:
            mark_path = os.path.join(utils.ICONS_PATH, "mark_not_valid.png")
            self.label_browser_valid_path_mark.setToolTip("Path is not valid for selected browser")

        # Mark for default path
        mark_icon = QtGui.QPixmap(mark_path)
        self.label_browser_valid_path_mark.setPixmap(mark_icon)

    def select_input_cache_path(self):
        """
        Slot for "button analyze default path" and for "button analyze other path".
        A path to analyze will be chosen and checked to be valid for selected browser.
        :return: nothing
        """

        # Clicked button ("default" or "other path")
        clicked_button = self.sender().objectName()

        # "Default" path button
        if clicked_button == "button_analyze_default_path":
            # Setting "current input path" as "default path"
            self.current_input_path = self.default_cache_path

            self.line_analysis_input_path.setText(self.current_input_path)
            self.line_analysis_input_path.home(False)

        # "Other path" button
        elif clicked_button == "button_analyze_other_path":
            # Selecting an input path to analyze
            dialog_input_path = QtGui.QFileDialog().getExistingDirectory(
                self, "Select a cache folder to analyze",
                os.path.join("C:", os.sep, "Users", unicode(os.environ['USERNAME']), "Desktop"),
                QtGui.QFileDialog.DontUseNativeDialog | QtGui.QFileDialog.ShowDirsOnly | QtGui.QFileDialog.ReadOnly
            )

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
                    # Browser name from table
                    browser = self.found_browsers_table_selection[0].text()

                    QtGui.QMessageBox.warning(
                        QtGui.QMessageBox(), "Wrong input path",
                        "{path} <br> is not correct for {browser}".format(path=dialog_input_path, browser=browser),
                        QtGui.QMessageBox.Ok
                    )

                # No selected path to analyze
                else:
                    QtGui.QMessageBox.information(
                        QtGui.QMessageBox(), "No selected path",
                        "Seems you did not select an input folder. <br> Please selected one",
                        QtGui.QMessageBox.Ok
                        )

        # Selected cache path info
        if self.current_input_path:
            # Info for current selected input path
            folder_info = utils.get_folder_info(folder_path=self.current_input_path)

            self.line_folder_dimension.setText(str(folder_info["folder_dimension"]))
            self.line_folder_elements.setText(str(folder_info["folder_elements"]))
            self.line_folder_creation_time.setText(str(folder_info["folder_creation_time"]))
            self.line_folder_last_access.setText(str(folder_info["folder_last_access_time"]))
            self.list_input_folder_preview.clear()
            self.list_input_folder_preview.addItems(os.listdir(self.current_input_path))

            self.button_confirm_analysis.setEnabled(True)

    def file_info(self):
        """
        Slot for "list input widget" in "folder choice screen".
        Calculating info about selected file from the list widget.
        :return: nothing
        """

        # Selected item from "list input folder" list widget
        selected_item = unicode(self.list_input_folder_preview.selectedItems()[0].text())
        file_path = os.path.join(self.current_input_path, selected_item)

        try:
            # Selected file info
            file_info = utils.get_file_info(file_path=file_path)

            self.line_file_selected.setText(selected_item)
            self.line_file_dimension.setText(str(file_info["file_dimension"]))
            self.line_file_creation_time.setText(str(file_info["creation_time"]))
            self.line_file_last_modified.setText(str(file_info["last_modified"]))
            self.line_file_last_access.setText(str(file_info["last_access"]))
            self.line_file_md5.setText(str(file_info["md5"]))
            self.line_file_sha1.setText(str(file_info["sha1"]))
        except Exception as _:
            QtGui.QMessageBox.critical(
                QtGui.QMessageBox(), "Error", "Unable to open file <br> {item}".format(item=selected_item),
                QtGui.QMessageBox.Ok
            )

############################
# SECTION: ANALYSIS SCREEN #
############################

    def set_analysis_screen(self):
        """
        Slot for "confirm and start analysis" button in "folder choice screen".
        Setting "analysis screen": stacked widget index = 3.
        :return:
        """

        self.stackedWidget.setCurrentIndex(3)
        self.progressBar_analysis.setValue(0)

        # Resetting table rows (if "analysis screen" already visited earlier)
        self.table_analysis_preview.setRowCount(0)

        self.line_input_path_analysis.setText(str(self.current_input_path.replace("/", "\\")))

        # Clipboard to store copied values from "table analysis preview"
        self.clipboard = QtGui.QApplication.clipboard()

        # Settings for buttons in "analysis screen"
        self.button_export_to_html.setEnabled(False)
        self.button_back_analysis_screen.setEnabled(False)
        self.button_stop_analysis_screen.setEnabled(True)

        # "Chrome analyzer thread"
        self.chrome_analyzer_thread = chrome.chrome_analyzer.ChromeAnalyzerThread(input_path=self.current_input_path)
        self.chrome_analyzer_thread.update_results_table_signal.connect(self.analysis_table_update)
        self.chrome_analyzer_thread.finished.connect(self.analysis_terminated)
        self.chrome_analyzer_thread.start()

    def analysis_table_update(self, num_elem, tot_elem, key_hash, key_data, content_type, creation_time):
        """
        Slot for "update results table" signal from "chrome analyzer thread".
        :param num_elem: position of the element in list of found cache entry instances.
        :param key_hash: hash of the key in found cache entry.
        :param key_data: data in cache entry.
        :param content_type: content type for the data in cache entry.
        :param creation_time: cache entry creation time.
        :return: nothing
        """

        # Insert cache entry values in "table analysis preview"
        self.table_analysis_preview.insertRow(num_elem)
        self.table_analysis_preview.setItem(num_elem, 0, QtGui.QTableWidgetItem(key_hash))
        self.table_analysis_preview.setItem(num_elem, 1, QtGui.QTableWidgetItem(key_data))
        self.table_analysis_preview.setItem(num_elem, 2, QtGui.QTableWidgetItem(content_type))
        self.table_analysis_preview.setItem(num_elem, 3, QtGui.QTableWidgetItem(creation_time))
        self.table_analysis_preview.scrollToBottom()

        # Copying "cache entries list" from "chrome analyzer thread" to avoid rescan for html export (if any).
        self.analysis_results_list = self.chrome_analyzer_thread.cache_entries_list[:]

        value = float(100 * len(self.analysis_results_list)) / float(tot_elem)
        self.progressBar_analysis.setValue(math.ceil(value))

    def table_results_context_menu(self, position):
        """
        Slot for mouse right click on "table analysis preview" to open a context menu for advanced results.
        :return:
        """

        menu = QtGui.QMenu()
        action_copy_to_clipboard = menu.addAction("Copy item to clipboard")
        action_advanced_results = menu.addAction("Show advanced results")
        action = menu.exec_(self.table_analysis_preview.mapToGlobal(position))

        if action == action_advanced_results:
            # Retrieving selected item from table "analysis preview"
            # Position in results list = table row
            current_table_row = self.table_analysis_preview.currentRow()
            current_result_item = self.analysis_results_list[current_table_row]

            # Opening a custom QDialog with file preview
            self.dialog_results_chrome = ChromeCustomDialog(item=current_result_item)
            self.dialog_results_chrome.exec_()

        if action == action_copy_to_clipboard:
            selection = self.table_analysis_preview.currentItem().text()
            self.clipboard.clear()
            self.clipboard.setText(selection)
            QtGui.QMessageBox.information(
                QtGui.QMessageBox(), "Clipboard",
                "{selection}\nElement copied to clipboard".format(selection=selection),
                QtGui.QMessageBox.Ok
            )

    def stop_analysis(self):
        """
        Slot for "stop analysis" button.
        Setting stop signal for "ChromeAnalyzerThread" to stop cache analysis.
        :return: nothing
        """

        # Setting stop signal
        self.chrome_analyzer_thread.stop_signal_analyzer.set()

    def analysis_terminated(self):
        """
        Slot for "finished signal" from "chrome analyzer thread".
        :return:
        """

        # Browser name from selection in "table found browser"
        browser_name = self.found_browsers_table_selection[0].text()

        # Analysis stopped by user
        if self.chrome_analyzer_thread.stopped_by_user:
            QtGui.QMessageBox.warning(
                QtGui.QMessageBox(), "Analysis stopped",
                "Analysis for {browser} stopped by user".format(browser=browser_name),
                QtGui.QMessageBox.Ok
            )

            # Settings for buttons in "analysis screen"
            self.button_stop_analysis_screen.setEnabled(False)
            self.button_back_analysis_screen.setEnabled(True)

        # Analysis complete
        else:

            if self.progressBar_analysis.value():
                self.progressBar_analysis.setValue(100)

            QtGui.QMessageBox.information(
                QtGui.QMessageBox(), "Analysis terminated",
                "Analysis for {browser} successfully terminated".format(browser=browser_name),
                QtGui.QMessageBox.Ok
            )

            # Settings for buttons in "analysis screen"
            self.button_export_to_html.setEnabled(True)
            self.button_stop_analysis_screen.setEnabled(False)
            self.button_back_analysis_screen.setEnabled(True)


###########################
# SECTION: EXPORT TO HTML #
###########################

    def export_to_html(self):

        # Selecting an output path for results
        dialog_output_path = QtGui.QFileDialog().getExistingDirectory(
            self, "Select an output path for results",
            os.path.join("C:", os.sep, "Users", unicode(os.environ['USERNAME']), "Desktop"),
            QtGui.QFileDialog.ShowDirsOnly
        )

        # Convert QString from QDialog to unicode
        self.current_output_path = unicode(dialog_output_path)

        if dialog_output_path:

            self.stackedWidget.setCurrentIndex(4)

            self.button_back_export_screen.setEnabled(False)
            self.button_stop_export_screen.setEnabled(True)

            self.line_input_path_exporting.setText(str(self.current_input_path.replace("/", "\\")))
            current_datetime = datetime.datetime.now().strftime("%d-%b-%Y-%H_%M_%S")
            scan_main_folder_name = "BrowserCacheAnalyzer-Scan[{date}]".format(date=current_datetime)
            complete_output_path = os.path.join(self.current_output_path, scan_main_folder_name)
            self.line_output_path_exporting.setText(str(complete_output_path.replace("/", "\\")))
            self.progressBar_exporting.setValue(0)

            self.chrome_export_thread = None
            self.chrome_export_thread = chrome.chrome_export.ChromeExportThread(
                input_path=self.current_input_path,
                output_path=self.current_output_path,
                scan_main_folder_name=scan_main_folder_name,
                entries_to_export=self.analysis_results_list,
                brw=self.found_browsers_table_selection[0].text(),
                brw_ver=self.found_browsers_table_selection[1].text(),
                brw_inst_path=self.found_browsers_table_selection[2].text(),
                brw_def_path=self.default_cache_path
            )
            self.chrome_export_thread.update_export_progress_signal.connect(self.export_progress_update)
            self.chrome_export_thread.finished.connect(self.export_terminated)
            self.chrome_export_thread.start()
        else:
            QtGui.QMessageBox.information(
                QtGui.QMessageBox(), "No selected path",
                "Seems you did not select an output folder. <br> Please selected one", QtGui.QMessageBox.Ok
            )

    def export_progress_update(self, exported_entries=None, tot_entries=None):

        value = float(100 * exported_entries) / float(tot_entries)
        self.progressBar_exporting.setValue(math.ceil(value))

    def stop_export(self):
        """
        Slot for "stop export" button.
        Setting stop signal for "ChromeExportThread" to stop results exporting.
        :return: nothing
        """

        # Setting stop signal
        self.chrome_export_thread.stop_signal_export.set()

    def export_terminated(self):
        """
        Slot for "finished signal" from "chrome export thread".
        :return:
        """

        # Browser name from selection in "table found browser"
        browser_name = self.found_browsers_table_selection[0].text()

        # Analysis stopped by user
        if self.chrome_export_thread.stopped_by_user:
            QtGui.QMessageBox.warning(
                QtGui.QMessageBox(), "Export stopped",
                "Export for {browser} stopped by user".format(browser=browser_name),
                QtGui.QMessageBox.Ok
            )

            # Settings for buttons in "analysis screen"
            self.button_back_export_screen.setEnabled(True)
            self.button_stop_export_screen.setEnabled(False)

        # Analysis complete
        else:

            if self.progressBar_exporting.value() < 100:
                self.progressBar_exporting.setValue(100)

            QtGui.QMessageBox.information(
                QtGui.QMessageBox(), "Export terminated",
                "Export for {browser} successfully terminated".format(browser=browser_name),
                QtGui.QMessageBox.Ok
            )

            # Settings for buttons in "analysis screen"
            self.button_stop_export_screen.setEnabled(False)
            self.button_back_export_screen.setEnabled(True)


#########################
# SECTION: EVENT FILTER #
#########################

    def eventFilter(self, q_object, q_event):
        """
        Filters events if this object has been installed as an event filter for the watched object.
        :param q_object: QObject
        :param q_event: QEvent
        :return: eventFilter(q_object, q_event)
        """

        # Mouse hover enter event
        if q_event.type() == QtCore.QEvent.HoverEnter:
            # "System info" groupBox
            if q_object in self.groupBox_system_info.findChildren(QtGui.QLineEdit):
                QtGui.QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.IBeamCursor))
            # "Selected browser" groupBox
            elif q_object in self.groupBox_selected_browser_info.findChildren(QtGui.QLineEdit):
                QtGui.QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.IBeamCursor))
            # "Found browser" groupBox
            elif q_object == self.groupBox_found_browsers:
                QtGui.QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
            # "Lines edit" in "analysis input folder" groupBox
            elif q_object in self.groupBox_analysis_input_folder.findChildren(QtGui.QLineEdit):
                if not q_object.text().isEmpty():
                    QtGui.QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.IBeamCursor))
            # "Lines edit" in "preview input folder" groupBox
            elif q_object in self.groupBox_preview_input_folder.findChildren(QtGui.QLineEdit):
                if not q_object.text().isEmpty():
                    QtGui.QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.IBeamCursor))
            # "Line input recap"
            elif q_object == self.line_input_path_analysis:
                    QtGui.QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.IBeamCursor))

        # Mouse hover leave event
        elif q_event.type() == QtCore.QEvent.HoverLeave:
            QtGui.QApplication.restoreOverrideCursor()

        elif q_event.type() == QtCore.QEvent.MouseButtonRelease:
            QtGui.QApplication.restoreOverrideCursor()

        # Pass the event on to the parent class
        return QtGui.QMainWindow.eventFilter(self, q_object, q_event)


##############################
# SECTION: CLOSE APPLICATION #
##############################

    def close_application(self):
        """
        Slot for application "close" button and "quit" button in "analysis screen".
        A message box will ask to confirm before quitting normally or during an analysis.
        :return: nothing
        """

        thread_running = None

        # If analyzer thread is running
        if self.chrome_analyzer_thread:
            thread_running = self.chrome_analyzer_thread.isRunning()

        # Checking clicked button
        clicked_button = self.sender().objectName()

        # Confirmation before quitting during an analysis
        if (thread_running and
                (clicked_button == "button_quit_analysis_screen" or clicked_button == "button_application_close")):

            browser_name = self.found_browsers_table_selection[0].text()

            msg_quit_analysis = QtGui.QMessageBox.question(
                QtGui.QMessageBox(), "Analysis running",
                "Analysis for {browser} is still running. Quit?".format(browser=browser_name),
                QtGui.QMessageBox.Yes | QtGui.QMessageBox.No, QtGui.QMessageBox.No
            )

            # If "yes" button clicked, quitting application
            if msg_quit_analysis == QtGui.QMessageBox.Yes:
                self.close()

        # Normal confirmation before quitting
        else:
            msg_confirm_exit = QtGui.QMessageBox.question(
                QtGui.QMessageBox(), "Confirm", "Are you sure you want to quit?",
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

    def __init__(self, parent=None, item=None):
        super(ChromeCustomDialog, self).__init__(parent)

        # Setting up the application user interface from python converted gui
        self.setupUi(self)

        # Settings for QDialog
        self.setStyleSheet("background-color: rgb(225,225,225) ")
        for button in self.findChildren(QtGui.QPushButton):
            button.setStyleSheet("QPushButton {background-color: transparent; border: 1px solid darkgray} "
                                 "QPushButton:hover {background-color: rgb(192,192,192) } ")

        for line in self.findChildren(QtGui.QLineEdit):
            line.installEventFilter(self)
            line.setReadOnly(True)
            line.setFrame(False)

        self.label_dialog_title.setTextInteractionFlags(QtCore.Qt.TextSelectableByMouse)

        # Values for selected item
        self.label_dialog_title.setText(str(item.key_hash))
        self.line_key_hash.setText(str(item.key_hash))
        self.line_next_entry_address.setText(str(item.next_entry_address))
        self.line_rank_node_address.setText(str(item.rankings_node_address))
        self.line_reuse_count.setText(str(item.reuse_count))
        self.line_refetch_count.setText(str(item.refetch_count))
        self.line_entry_state.setText(str(item.entry_state))
        self.line_creation_time.setText(str(item.creation_time))
        self.line_key_data_size.setText(str(item.key_data_size))
        self.line_long_key_address.setText(str(item.long_key_data_address))
        self.line_cache_entry_flags.setText(str(item.cache_entry_flags))
        self.line_key_data.setText(str(item.key_data))
        self.line_key_data.home(False)

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

    def eventFilter(self, q_object, q_event):

        # Restoring default cursor shape when leaving object
        QtGui.QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))

        # Lines edit
        if q_event.type() == QtCore.QEvent.HoverMove \
                and q_object in self.findChildren(QtGui.QLineEdit):
            QtGui.QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.IBeamCursor))

        return QtGui.QMainWindow.eventFilter(self, q_object, q_event)
