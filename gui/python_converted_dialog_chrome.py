# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui\dialog_results_chrome.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_DialogResultsChrome(object):
    def setupUi(self, DialogResultsChrome):
        DialogResultsChrome.setObjectName(_fromUtf8("DialogResultsChrome"))
        DialogResultsChrome.resize(600, 400)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(DialogResultsChrome.sizePolicy().hasHeightForWidth())
        DialogResultsChrome.setSizePolicy(sizePolicy)
        DialogResultsChrome.setMinimumSize(QtCore.QSize(600, 400))
        DialogResultsChrome.setMaximumSize(QtCore.QSize(600, 500))
        self.gridLayout_3 = QtGui.QGridLayout(DialogResultsChrome)
        self.gridLayout_3.setObjectName(_fromUtf8("gridLayout_3"))
        self.gridLayout_2 = QtGui.QGridLayout()
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.label_2 = QtGui.QLabel(DialogResultsChrome)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Source Sans Pro"))
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout_2.addWidget(self.label_2, 0, 0, 1, 1)
        self.label_res_key_hash = QtGui.QLabel(DialogResultsChrome)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Source Sans Pro"))
        font.setPointSize(11)
        self.label_res_key_hash.setFont(font)
        self.label_res_key_hash.setText(_fromUtf8(""))
        self.label_res_key_hash.setObjectName(_fromUtf8("label_res_key_hash"))
        self.gridLayout_2.addWidget(self.label_res_key_hash, 0, 1, 1, 1)
        self.label_3 = QtGui.QLabel(DialogResultsChrome)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Source Sans Pro"))
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.label_3.setFont(font)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.gridLayout_2.addWidget(self.label_3, 1, 0, 1, 1)
        self.label_res_next_entry_address = QtGui.QLabel(DialogResultsChrome)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Source Sans Pro"))
        font.setPointSize(11)
        self.label_res_next_entry_address.setFont(font)
        self.label_res_next_entry_address.setText(_fromUtf8(""))
        self.label_res_next_entry_address.setObjectName(_fromUtf8("label_res_next_entry_address"))
        self.gridLayout_2.addWidget(self.label_res_next_entry_address, 1, 1, 1, 1)
        self.label_4 = QtGui.QLabel(DialogResultsChrome)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Source Sans Pro"))
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.label_4.setFont(font)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.gridLayout_2.addWidget(self.label_4, 2, 0, 1, 1)
        self.label_res_rank_node_address = QtGui.QLabel(DialogResultsChrome)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Source Sans Pro"))
        font.setPointSize(11)
        self.label_res_rank_node_address.setFont(font)
        self.label_res_rank_node_address.setText(_fromUtf8(""))
        self.label_res_rank_node_address.setObjectName(_fromUtf8("label_res_rank_node_address"))
        self.gridLayout_2.addWidget(self.label_res_rank_node_address, 2, 1, 1, 1)
        self.label_5 = QtGui.QLabel(DialogResultsChrome)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Source Sans Pro"))
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.label_5.setFont(font)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.gridLayout_2.addWidget(self.label_5, 3, 0, 1, 1)
        self.label_res_reuse_count = QtGui.QLabel(DialogResultsChrome)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Source Sans Pro"))
        font.setPointSize(11)
        self.label_res_reuse_count.setFont(font)
        self.label_res_reuse_count.setText(_fromUtf8(""))
        self.label_res_reuse_count.setObjectName(_fromUtf8("label_res_reuse_count"))
        self.gridLayout_2.addWidget(self.label_res_reuse_count, 3, 1, 1, 1)
        self.label_6 = QtGui.QLabel(DialogResultsChrome)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Source Sans Pro"))
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.label_6.setFont(font)
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.gridLayout_2.addWidget(self.label_6, 4, 0, 1, 1)
        self.label_res_refetch_count = QtGui.QLabel(DialogResultsChrome)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Source Sans Pro"))
        font.setPointSize(11)
        self.label_res_refetch_count.setFont(font)
        self.label_res_refetch_count.setText(_fromUtf8(""))
        self.label_res_refetch_count.setObjectName(_fromUtf8("label_res_refetch_count"))
        self.gridLayout_2.addWidget(self.label_res_refetch_count, 4, 1, 1, 1)
        self.label_7 = QtGui.QLabel(DialogResultsChrome)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Source Sans Pro"))
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.label_7.setFont(font)
        self.label_7.setObjectName(_fromUtf8("label_7"))
        self.gridLayout_2.addWidget(self.label_7, 5, 0, 1, 1)
        self.label_res_entry_state = QtGui.QLabel(DialogResultsChrome)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Source Sans Pro"))
        font.setPointSize(11)
        self.label_res_entry_state.setFont(font)
        self.label_res_entry_state.setText(_fromUtf8(""))
        self.label_res_entry_state.setObjectName(_fromUtf8("label_res_entry_state"))
        self.gridLayout_2.addWidget(self.label_res_entry_state, 5, 1, 1, 1)
        self.label_8 = QtGui.QLabel(DialogResultsChrome)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Source Sans Pro"))
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.label_8.setFont(font)
        self.label_8.setObjectName(_fromUtf8("label_8"))
        self.gridLayout_2.addWidget(self.label_8, 6, 0, 1, 1)
        self.label_res_creation_time = QtGui.QLabel(DialogResultsChrome)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Source Sans Pro"))
        font.setPointSize(11)
        self.label_res_creation_time.setFont(font)
        self.label_res_creation_time.setText(_fromUtf8(""))
        self.label_res_creation_time.setObjectName(_fromUtf8("label_res_creation_time"))
        self.gridLayout_2.addWidget(self.label_res_creation_time, 6, 1, 1, 1)
        self.label_9 = QtGui.QLabel(DialogResultsChrome)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Source Sans Pro"))
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.label_9.setFont(font)
        self.label_9.setObjectName(_fromUtf8("label_9"))
        self.gridLayout_2.addWidget(self.label_9, 7, 0, 1, 1)
        self.label_res_key_data_size = QtGui.QLabel(DialogResultsChrome)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Source Sans Pro"))
        font.setPointSize(11)
        self.label_res_key_data_size.setFont(font)
        self.label_res_key_data_size.setText(_fromUtf8(""))
        self.label_res_key_data_size.setObjectName(_fromUtf8("label_res_key_data_size"))
        self.gridLayout_2.addWidget(self.label_res_key_data_size, 7, 1, 1, 1)
        self.label_10 = QtGui.QLabel(DialogResultsChrome)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Source Sans Pro"))
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.label_10.setFont(font)
        self.label_10.setObjectName(_fromUtf8("label_10"))
        self.gridLayout_2.addWidget(self.label_10, 8, 0, 1, 1)
        self.label_res_long_key_address = QtGui.QLabel(DialogResultsChrome)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Source Sans Pro"))
        font.setPointSize(11)
        self.label_res_long_key_address.setFont(font)
        self.label_res_long_key_address.setText(_fromUtf8(""))
        self.label_res_long_key_address.setObjectName(_fromUtf8("label_res_long_key_address"))
        self.gridLayout_2.addWidget(self.label_res_long_key_address, 8, 1, 1, 1)
        self.label_11 = QtGui.QLabel(DialogResultsChrome)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Source Sans Pro"))
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.label_11.setFont(font)
        self.label_11.setObjectName(_fromUtf8("label_11"))
        self.gridLayout_2.addWidget(self.label_11, 9, 0, 1, 1)
        self.label_res_cache_entry_flags = QtGui.QLabel(DialogResultsChrome)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Source Sans Pro"))
        font.setPointSize(11)
        self.label_res_cache_entry_flags.setFont(font)
        self.label_res_cache_entry_flags.setText(_fromUtf8(""))
        self.label_res_cache_entry_flags.setObjectName(_fromUtf8("label_res_cache_entry_flags"))
        self.gridLayout_2.addWidget(self.label_res_cache_entry_flags, 9, 1, 1, 1)
        self.label_12 = QtGui.QLabel(DialogResultsChrome)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Source Sans Pro"))
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.label_12.setFont(font)
        self.label_12.setObjectName(_fromUtf8("label_12"))
        self.gridLayout_2.addWidget(self.label_12, 10, 0, 1, 1)
        self.line_res_key_data = QtGui.QLineEdit(DialogResultsChrome)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Source Sans Pro"))
        font.setPointSize(11)
        self.line_res_key_data.setFont(font)
        self.line_res_key_data.setObjectName(_fromUtf8("line_res_key_data"))
        self.gridLayout_2.addWidget(self.line_res_key_data, 10, 1, 1, 1)
        self.gridLayout_3.addLayout(self.gridLayout_2, 2, 0, 1, 1)
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.label_dialog_title = QtGui.QLabel(DialogResultsChrome)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Source Sans Pro"))
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.label_dialog_title.setFont(font)
        self.label_dialog_title.setText(_fromUtf8(""))
        self.label_dialog_title.setObjectName(_fromUtf8("label_dialog_title"))
        self.gridLayout.addWidget(self.label_dialog_title, 0, 2, 1, 1)
        self.button_dialog_close = QtGui.QPushButton(DialogResultsChrome)
        self.button_dialog_close.setMinimumSize(QtCore.QSize(24, 24))
        self.button_dialog_close.setMaximumSize(QtCore.QSize(24, 24))
        self.button_dialog_close.setText(_fromUtf8(""))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/button_close.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.button_dialog_close.setIcon(icon)
        self.button_dialog_close.setIconSize(QtCore.QSize(24, 24))
        self.button_dialog_close.setObjectName(_fromUtf8("button_dialog_close"))
        self.gridLayout.addWidget(self.button_dialog_close, 0, 4, 1, 1)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 0, 3, 1, 1)
        self.label = QtGui.QLabel(DialogResultsChrome)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Source Sans Pro"))
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        spacerItem1 = QtGui.QSpacerItem(20, 20, QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem1, 0, 1, 1, 1)
        self.gridLayout_3.addLayout(self.gridLayout, 0, 0, 1, 1)
        spacerItem2 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        self.gridLayout_3.addItem(spacerItem2, 1, 0, 1, 1)

        self.retranslateUi(DialogResultsChrome)
        QtCore.QMetaObject.connectSlotsByName(DialogResultsChrome)

    def retranslateUi(self, DialogResultsChrome):
        DialogResultsChrome.setWindowTitle(_translate("DialogResultsChrome", "Dialog", None))
        self.label_2.setText(_translate("DialogResultsChrome", "Key hash:", None))
        self.label_3.setText(_translate("DialogResultsChrome", "Next entry address:", None))
        self.label_4.setText(_translate("DialogResultsChrome", "Rankings node adrress:", None))
        self.label_5.setText(_translate("DialogResultsChrome", "Reuse count:", None))
        self.label_6.setText(_translate("DialogResultsChrome", "Refetch count:", None))
        self.label_7.setText(_translate("DialogResultsChrome", "Entry state:", None))
        self.label_8.setText(_translate("DialogResultsChrome", "Creation time:", None))
        self.label_9.setText(_translate("DialogResultsChrome", "Key data size (bytes):", None))
        self.label_10.setText(_translate("DialogResultsChrome", "Long key data address:", None))
        self.label_11.setText(_translate("DialogResultsChrome", "Cache entry flags:", None))
        self.label_12.setText(_translate("DialogResultsChrome", "Key data:", None))
        self.label.setText(_translate("DialogResultsChrome", "Advanced info for entry:", None))

import icons_rc
