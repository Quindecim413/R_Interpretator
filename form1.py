from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QInputDialog, QLineEdit, QWidget
import sys
import os
from parsimonious.grammar import Grammar
import visitor
from node_rules import *


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 768)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox.setTitle("")
        self.groupBox.setFlat(False)
        self.groupBox.setObjectName("groupBox")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.groupBox)
        self.verticalLayout.setObjectName("verticalLayout")
        self.tree_text = QtWidgets.QTextEdit(self.groupBox)
        self.tree_text.setObjectName("tree_text")
        self.tree_text.setReadOnly(True)

        self.tree_text.setStyleSheet("color: black;")
        self.verticalLayout.addWidget(self.tree_text)
        self.code_text = QtWidgets.QTextEdit(self.groupBox)
        self.code_text.setEnabled(True)
        self.code_text.setObjectName("code_text")
        self.verticalLayout.addWidget(self.code_text)
        self.horizontalLayout_2.addWidget(self.groupBox)
        self.groupBox_2 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_2.setTitle("")
        self.groupBox_2.setObjectName("groupBox_2")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.groupBox_2)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.groupBox_3 = QtWidgets.QGroupBox(self.groupBox_2)
        self.groupBox_3.setEnabled(True)
        self.groupBox_3.setTitle("")
        self.groupBox_3.setObjectName("groupBox_3")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.groupBox_3)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.ast_button = QtWidgets.QPushButton(self.groupBox_3)
        self.ast_button.setObjectName("ast_button")
        self.horizontalLayout.addWidget(self.ast_button)
        self.var_button = QtWidgets.QPushButton(self.groupBox_3)
        self.var_button.setObjectName("var_button")
        self.horizontalLayout.addWidget(self.var_button)
        self.verticalLayout_3.addWidget(self.groupBox_3)
        self.var_ast_text = QtWidgets.QTextEdit(self.groupBox_2)
        self.var_ast_text.setEnabled(True)
        self.var_ast_text.setReadOnly(True)
        self.var_ast_text.setStyleSheet("color: black;")
        self.verticalLayout_3.addWidget(self.var_ast_text)
        self.groupBox_4 = QtWidgets.QGroupBox(self.groupBox_2)
        self.groupBox_4.setTitle("")
        self.groupBox_4.setObjectName("groupBox_4")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.groupBox_4)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.clean_button = QtWidgets.QPushButton(self.groupBox_4)
        self.clean_button.setObjectName("clean_button")
        self.verticalLayout_2.addWidget(self.clean_button)
        self.file_button = QtWidgets.QPushButton(self.groupBox_4)
        self.file_button.setObjectName("file_button")
        self.verticalLayout_2.addWidget(self.file_button)
        self.code_button = QtWidgets.QPushButton(self.groupBox_4)
        self.code_button.setObjectName("code_button")
        self.verticalLayout_2.addWidget(self.code_button)
        self.verticalLayout_3.addWidget(self.groupBox_4)
        self.horizontalLayout_2.addWidget(self.groupBox_2)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))

        self.ast_button.setText(_translate("MainWindow", "AST дерево"))
        self.ast_button.clicked.connect(self.AstButtonClicked)

        self.var_button.setText(_translate("MainWindow", "Переменные"))
        self.var_button.clicked.connect(self.VarButtonClicked)

        self.clean_button.setText(_translate("MainWindow", "Очистить"))
        self.clean_button.clicked.connect(self.CleanButtonClicked)

        self.file_button.setText(_translate("MainWindow", "Загрузить из файла"))
        self.file_button.clicked.connect(self.FileButtonClicked)

        self.code_button.setText(_translate("MainWindow", "Выполнить код"))
        self.code_button.clicked.connect(self.CodeButtonClicked)

    def FileButtonClicked(self):
        print("FileButtonClicked")
        QInputDialog.getText(self, "", "")
        # text, okPressed = QInputDialog.getText(QWidget, 'Text Input Dialog', 'Enter your name:')
        # if okPressed and text != '':
        #     print(text)

    def CodeButtonClicked(self):
        print("CodeButtonClicked")
        self.var_ast_text.setText("asdfghjk")
        self.tree_text.setText("qqqqqqqqq")
        # inp = open('test.r').read()
        inp = self.code_text.toPlainText()
        parse_tree = grammar.parse(inp)
        v = Start.create(None, visitor.Visitor().visit(parse_tree), parse_tree.start, parse_tree.end)
        self.var_ast_text.setText(str(v))

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
    fls = list(sorted([f for f in os.listdir('.') if not f.startswith('.')]))
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()

    gr = open('grammar.peg').read()
    grammar = Grammar(gr)

    sys.exit(app.exec_())