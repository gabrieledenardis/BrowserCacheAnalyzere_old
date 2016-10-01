# -*- coding: utf-8 -*-
# !/usr/bin/env python

# PyQt4 imports
from PyQt4 import QtGui, QtCore

# Python imports
import platform

# Project imports
from gui import python_converted_gui


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

    #######################
    # SECTION: ATTRIBUTES #
    #######################

        # Mouse cursor coordinates on left click over the application window
        self.mouse_press_position = None

    ##########################################
    # SECTION: SIGNALS AND SLOTS CONNECTIONS #
    ##########################################

        # Application "minimize" and "close" buttons
        self.button_application_minimize.clicked.connect(self.showMinimized)
        self.button_application_close.clicked.connect(self.close_application)

        # Other application elements
        self.button_welcome_screen_next.clicked.connect(self.set_browser_choice_screen)

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

        # "System info" values
        self.line_system_os_name.setText(platform.system())
        self.line_system_release.setText(platform.release())
        self.line_system_release_version.setText(platform.version())
        self.line_system_hostname.setText(platform.node())

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
