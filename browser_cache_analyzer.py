# -*- coding: utf-8 -*-
# !/usr/bin/env python

# PyQt4 imports
from PyQt4 import QtGui, QtCore

# Project imports
from gui import python_converted_gui


class BrowserCacheAnalyzer(QtGui.QMainWindow, python_converted_gui.Ui_AnalyzerMainWindow):

    def __init__(self, parent=None):
        super(BrowserCacheAnalyzer, self).__init__(parent)

        # Setting up the application user interface from python converted gui
        self.setupUi(self)

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

    ###########################
    # SECTION: WELCOME SCREEN #
    ###########################

        # Setting "welcome screen" as application start screen
        self.stackedWidget.setCurrentIndex(0)

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
