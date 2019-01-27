# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/Users/balagnese/Desktop/form2.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from parsimonious.grammar import Grammar
import visitor
from node_rules import *

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(790, 769)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.code_text = QtWidgets.QTextEdit(self.centralwidget)
        self.code_text.setObjectName("code_text")
        self.gridLayout.addWidget(self.code_text, 5, 0, 1, 1)
        self.exec_code_text = QtWidgets.QTextEdit(self.centralwidget)
        self.exec_code_text.setObjectName("exec_code_text")
        self.exec_code_text.setReadOnly(True)
        self.gridLayout.addWidget(self.exec_code_text, 3, 0, 1, 1)
        self.file_button = QtWidgets.QPushButton(self.centralwidget)
        self.file_button.setObjectName("file_button")
        self.gridLayout.addWidget(self.file_button, 1, 1, 1, 1)
        self.clean_button = QtWidgets.QPushButton(self.centralwidget)
        self.clean_button.setObjectName("clean_button")
        self.gridLayout.addWidget(self.clean_button, 0, 1, 1, 1)
        self.var_text = QtWidgets.QTextEdit(self.centralwidget)
        self.var_text.setObjectName("var_text")
        self.var_text.setReadOnly(True)
        self.gridLayout.addWidget(self.var_text, 5, 1, 1, 1)
        self.ast_text = QtWidgets.QTextEdit(self.centralwidget)
        self.ast_text.setObjectName("ast_text")
        self.ast_text.setReadOnly(True)
        self.gridLayout.addWidget(self.ast_text, 3, 1, 1, 1)
        self.code_button = QtWidgets.QPushButton(self.centralwidget)
        self.code_button.setObjectName("code_button")
        self.gridLayout.addWidget(self.code_button, 0, 0, 2, 1)
        self.exec_code_label = QtWidgets.QLabel(self.centralwidget)
        self.exec_code_label.setObjectName("exec_code_label")
        self.gridLayout.addWidget(self.exec_code_label, 2, 0, 1, 1)
        self.code_label = QtWidgets.QLabel(self.centralwidget)
        self.code_label.setObjectName("code_label")
        self.gridLayout.addWidget(self.code_label, 4, 0, 1, 1)
        self.ast_label = QtWidgets.QLabel(self.centralwidget)
        self.ast_label.setObjectName("ast_label")
        self.gridLayout.addWidget(self.ast_label, 2, 1, 1, 1)
        self.var_label = QtWidgets.QLabel(self.centralwidget)
        self.var_label.setObjectName("var_label")
        self.gridLayout.addWidget(self.var_label, 4, 1, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.file_button.setText(_translate("MainWindow", "Загрузить из файла"))
        self.clean_button.setText(_translate("MainWindow", "Очистить"))
        self.code_button.setText(_translate("MainWindow", "Выполнить код"))
        self.code_button.clicked.connect(self.CodeButtonClicked)
        self.exec_code_label.setText(_translate("MainWindow", "Исполенный код"))
        self.code_label.setText(_translate("MainWindow", "Пишите код"))
        self.ast_label.setText(_translate("MainWindow", "AST"))
        self.var_label.setText(_translate("MainWindow", "Переменные"))

    def FileButtonClicked(self):
        print("FileButtonClicked")


    def CodeButtonClicked(self):
        print("CodeButtonClicked")

        self.ast_text.setText("asdfghjk")
        self.var_text.setText("qqqqqqqqq")
        self.exec_code_text.setText('awsdfghj')
        self.code_text.setText("zsdxfcghjlk;")
        print("ok")
        # inp = open('test.r').read()

        # parse_tree = grammar.parse(inp)
        # v = Start.create(None, visitor.Visitor().visit(parse_tree), parse_tree.start, parse_tree.end)
        # self.var_ast_text.setText(str(v))

    def CleanButtonClicked(self):
        print("CleanButtonClicked")
        self.tree_text.setText("")
        self.code_text.setText("")
        self.var_ast_text.setText("")

    def VarButtonClicked(self):
        print("VarButtonClicked")

    def AstButtonClicked(self):
        print("AstButtonClicked")


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    gr = open('grammar.peg').read()
    grammar = Grammar(gr)
    sys.exit(app.exec_())

