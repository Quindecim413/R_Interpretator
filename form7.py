# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/Users/balagnese/Desktop/form7.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QFileDialog, QWidget
from parsimonious.grammar import Grammar
import visitor
from node_rules import *

class Ui_QWidget(QWidget):
    def setupUi(self, QWidget):
        QWidget.setObjectName("QWidget")
        QWidget.resize(816, 702)
        self.centralwidget = QtWidgets.QWidget(QWidget)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox.setTitle("")
        self.groupBox.setObjectName("groupBox")
        self.gridLayout = QtWidgets.QGridLayout(self.groupBox)
        self.gridLayout.setObjectName("gridLayout")
        self.exec_code_label = QtWidgets.QLabel(self.groupBox)
        self.exec_code_label.setObjectName("exec_code_label")
        self.gridLayout.addWidget(self.exec_code_label, 4, 0, 1, 1)
        self.var_text = QtWidgets.QTextEdit(self.groupBox)
        self.var_text.setObjectName("var_text")
        self.var_text.setReadOnly(True)
        self.gridLayout.addWidget(self.var_text, 7, 1, 1, 1)
        self.ast_label = QtWidgets.QLabel(self.groupBox)
        self.ast_label.setObjectName("ast_label")
        self.gridLayout.addWidget(self.ast_label, 4, 1, 1, 1)
        self.code_label = QtWidgets.QLabel(self.groupBox)
        self.code_label.setObjectName("code_label")
        self.gridLayout.addWidget(self.code_label, 6, 0, 1, 1)
        self.exec_code_text = QtWidgets.QTextEdit(self.groupBox)
        self.exec_code_text.setObjectName("exec_code_text")
        self.exec_code_text.setReadOnly(True)
        self.gridLayout.addWidget(self.exec_code_text, 5, 0, 1, 1)
        self.var_label = QtWidgets.QLabel(self.groupBox)
        self.var_label.setObjectName("var_label")
        self.gridLayout.addWidget(self.var_label, 6, 1, 1, 1)
        self.code_text = QtWidgets.QTextEdit(self.groupBox)
        self.code_text.setObjectName("code_text")
        self.gridLayout.addWidget(self.code_text, 7, 0, 1, 1)
        self.code_button = QtWidgets.QPushButton(self.groupBox)
        self.code_button.setEnabled(True)
        self.code_button.setObjectName("code_button")
        self.gridLayout.addWidget(self.code_button, 0, 0, 1, 1)
        self.ast_text = QtWidgets.QTextEdit(self.groupBox)
        self.ast_text.setObjectName("ast_text")
        self.ast_text.setReadOnly(True)
        self.gridLayout.addWidget(self.ast_text, 5, 1, 1, 1)
        self.file_button = QtWidgets.QPushButton(self.groupBox)
        self.file_button.setObjectName("file_button")
        self.gridLayout.addWidget(self.file_button, 0, 1, 1, 1)
        self.save_button = QtWidgets.QPushButton(self.groupBox)
        self.save_button.setObjectName("save_button")
        self.gridLayout.addWidget(self.save_button, 1, 1, 1, 1)
        self.clean_button = QtWidgets.QPushButton(self.groupBox)
        self.clean_button.setObjectName("clean_button")
        self.gridLayout.addWidget(self.clean_button, 1, 0, 1, 1)
        self.horizontalLayout.addWidget(self.groupBox)
        QWidget.setCentralWidget(self.centralwidget)

        self.retranslateUi(QWidget)
        QtCore.QMetaObject.connectSlotsByName(QWidget)

    def retranslateUi(self, QWidget):
        _translate = QtCore.QCoreApplication.translate
        QWidget.setWindowTitle(_translate("QWidget", "QWidget"))
        self.exec_code_label.setText(_translate("QWidget", "Исполенный код"))
        self.ast_label.setText(_translate("QWidget", "AST"))
        self.code_label.setText(_translate("QWidget", "Пишите код"))
        self.var_label.setText(_translate("QWidget", "Переменные"))

        self.code_button.setText(_translate("QWidget", "Выполнить код"))
        self.code_button.clicked.connect(self.CodeButtonClicked)

        self.file_button.setText(_translate("QWidget", "Загрузить из файла"))
        self.file_button.clicked.connect(self.FileButtonClicked)

        self.save_button.setText(_translate("QWidget", "Сохранить в файл"))
        self.save_button.clicked.connect(self.SaveButtonClicked)

        self.clean_button.setText(_translate("QWidget", "Очистить"))
        self.clean_button.clicked.connect(self.CleanButtonClicked)

    def FileButtonClicked(self):
        print("FileButtonClicked")
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileName()", "",
                                                  "All Files (*);;R Files (*.r)", options=options)
        if fileName:
            print(fileName)
            text = open(fileName).read()
            self.code_text.setText(text)

    def CodeButtonClicked(self):
        print("CodeButtonClicked")
        # inp = open('test.r').read()
        inp = self.code_text.toPlainText()
        parse_tree = grammar.parse(inp)
        v = Start.create(None, visitor.Visitor().visit(parse_tree), parse_tree.start, parse_tree.end)
        self.ast_text.setText(str(v))


    def CleanButtonClicked(self):
        print("CleanButtonClicked")
        # self.ast_text.setText("")
        # self.code_text.setText("")
        # self.var_text.setText("")
        # self.exec_code_text.setText("")

    def SaveButtonClicked(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getSaveFileName(self, "QFileDialog.getSaveFileName()", "",
                                                  "All Files (*);;R Files (*.r)", options=options)
        if fileName:
            print(fileName)
            text = self.code_text.toPlainText()
            with open(fileName, 'w') as f:
                f.write(text)


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_QWidget()
    ui.setupUi(MainWindow)
    MainWindow.show()

    gr = open('grammar.peg').read()
    grammar = Grammar(gr)

    sys.exit(app.exec_())

