from PyQt5.QtCore import QDate, QFile, Qt, QTextStream
from PyQt5.QtGui import (QFont, QIcon, QKeySequence, QTextCharFormat,
                         QTextCursor, QTextTableFormat)
from PyQt5.QtWidgets import (QAction, QApplication, QDialog, QDockWidget, QFileDialog,
                             QFileDialog, QListWidget, QMainWindow, QMessageBox, QTextEdit)
import iconos_rc

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.filename = ""
        self.textEdit = QTextEdit()
        font = QFont("asdsadas")
        font.setPointSize(18)
        self.textEdit.setFont(font)
        self.setCentralWidget(self.textEdit)
        # Configuraciones
        self.createActions()
        self.createMenus()
        self.createToolBars()
        self.createStatusBar()
        self.createDockWindows()
        self.setWindowTitle("Programa chido")
        self.resetTextEdit()
        #self.newFile()

    def newFile(self):
        # Revisa si hay cambios
        if (self.findChanges or self.filename is "") and self.textEdit.toPlainText():
            self.ChangesBox()
        else:
            self.resetTextEdit()

    def resetTextEdit(self):
        self.textEdit.clear()

        cursor = self.textEdit.textCursor()
        cursor.movePosition(QTextCursor.Start)

        topFrame = cursor.currentFrame()

        topFrameFormat = topFrame.frameFormat()
        topFrameFormat.setPadding(18)
        topFrame.setFrameFormat(topFrameFormat)

    @property
    def findChanges(self):
        document = self.textEdit.document()
        return document.isModified()

    def ChangesBox(self):
        msgBox = QMessageBox()
        msgBox.setText("El documento ha sido modificado.")
        msgBox.setInformativeText("Quieres guardar los cambios?")
        msgBox.setStandardButtons(QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel)
        msgBox.setDefaultButton(QMessageBox.Save)

        res = msgBox.exec()
        if res == QMessageBox.Save:
            if self.filename == "":
                self.saveFileAsf()
                self.resetTextEdit()
            else:
                self.saveFilef()
                self.resetTextEdit()
                self.filename = ""
        elif res == QMessageBox.Discard:
            self.resetTextEdit()
            self.filename = ""
        elif res == QMessageBox.Cancel:
            return

    def saveFilef(self):
        if self.filename != "":
            file = QFile(self.filename)
            if not file.open(QFile.WriteOnly | QFile.Text):
                QMessageBox.warning(self, "Archivo",
                                    "No se pudo crear el archivo %s:\n%s." % (self.filename, file.errorString()))
                return

            out = QTextStream(file)
            QApplication.setOverrideCursor(Qt.WaitCursor)
            out << self.textEdit.toPlainText()
            QApplication.restoreOverrideCursor()

            self.statusBar().showMessage("Archivo '%s' guardado." % self.filename, 2500)
        else:
            self.saveFileAsf()

    def saveFileAsf(self):
        self.filename, _ = QFileDialog.getSaveFileName(self,
                                                  "Guardar como...", '.', "Sic standar (*.s)")
        if not self.filename:
            return

        file = QFile(self.filename)
        if not file.open(QFile.WriteOnly | QFile.Text):
            QMessageBox.warning(self, "Archivo",
                                "No se pudo crear el archivo %s:\n%s." % (self.filename, file.errorString()))
            self.filename = ""
            return

        out = QTextStream(file)
        QApplication.setOverrideCursor(Qt.WaitCursor)
        out << self.textEdit.toPlainText()
        QApplication.restoreOverrideCursor()

        self.statusBar().showMessage("Archivo '%s' guardado." % self.filename, 2500)

    def openFilef(self):
        self.filename, _ = QFileDialog.getOpenFileName(self,
                                                  "Guardar como...", '.', "Sic standar (*.s)")
        if not self.filename:
            return

        file = QFile(self.filename)
        if not file.open(QFile.ReadOnly | QFile.Text):
            QMessageBox.warning(self, "Archivo",
                                "No se pudo abrir el archivo %s:\n%s." % (self.filename, file.errorString()))
            return

        inn = QTextStream(file)
        self.newFile()
        self.textEdit.append(inn.readAll())
        self.statusBar().showMessage("Archivo '%s' cargado." % self.filename, 2500)

    def undof(self):
        document = self.textEdit.document()
        document.undo()

    def assembleCodef(self):
        pass

    def simulateCode(self):
        pass

    def createActions(self):
        self.newFilea = QAction(QIcon(':/iconos/documento.png'), "&Nuevo", self, shortcut=QKeySequence.New,
                                statusTip="Crea un nuevo documento", triggered=self.newFile)

        self.saveFile = QAction(QIcon(':/iconos/guardar.png'), "&Guardar", self, shortcut=QKeySequence.Save,
                                statusTip="Guarda el documento actual", triggered=self.saveFilef)

        self.openFile = QAction(QIcon(':/iconos/abrir-archivo.png'), "&Abrir", self, shortcut=QKeySequence.Open,
                                statusTip="Abre un archivo", triggered=self.openFilef)

        self.undo = QAction(QIcon(':/iconos/deshacer.png'), "&Deshacer", self, shortcut=QKeySequence.Undo,
                            statusTip="Regresa un cambio", triggered=self.undof)

        self.saveAsFile = QAction(QIcon(':/iconos/guardar-como.png'), "&Guardar como...", self,
                                  shortcut=QKeySequence.SaveAs,
                                  statusTip="Guarda el documento actual en un lugar especificado",
                                  triggered=self.saveFileAsf)

        self.assembleCode = QAction(QIcon(':/iconos/ensamblar.png'), "Ensamblar", self, shortcut="F5",
                                    statusTip="Ensamblar el documento actual")

        self.simulateCode = QAction(QIcon(':/iconos/simular.png'), "Simular", self, shortcut="Ctrl+F5",
                                    statusTip="Simula el documento actual")

        self.quit = QAction("Salir", self, shortcut=QKeySequence.Quit, statusTip="Cierra la aplicación",
                            triggered=self.close)

    def createMenus(self):
        self.fileMenu = self.menuBar().addMenu("Nuevo")
        self.fileMenu.addAction(self.newFilea)
        self.fileMenu.addAction(self.openFile)
        self.fileMenu.addSeparator()
        self.fileMenu.addAction(self.saveFile)
        self.fileMenu.addAction(self.saveAsFile)
        self.fileMenu.addSeparator()
        self.fileMenu.addAction(self.quit)

        self.editMenu = self.menuBar().addMenu("Editar")
        self.editMenu.addAction(self.undo)

        self.viewMenu = self.menuBar().addMenu("Ventanas")

        self.menuBar().addSeparator()

    def createToolBars(self):
        self.fileToolBar = self.addToolBar("Archivo")
        self.fileToolBar.addAction(self.newFilea)
        self.fileToolBar.addAction(self.saveFile)

        self.editToolBar = self.addToolBar("Editar")
        self.editToolBar.addAction(self.undo)

        self.processToolBar = self.addToolBar("Procesar")
        self.processToolBar.addAction(self.assembleCode)
        self.processToolBar.addAction(self.simulateCode)

    def createStatusBar(self):
        self.statusBar().showMessage("Listo")

    def createDockWindows(self):
        dock = QDockWidget("Archivo intermedio", self)
        #dock.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)
        self.customerList = QListWidget(dock)
        dock.setWidget(self.customerList)
        self.addDockWidget(Qt.RightDockWidgetArea, dock)
        self.viewMenu.addAction(dock.toggleViewAction())

        dock = QDockWidget("Tabla de símbolos", self)
        self.paragraphsList = QListWidget(dock)
        dock.setWidget(self.paragraphsList)
        self.addDockWidget(Qt.RightDockWidgetArea, dock)
        self.viewMenu.addAction(dock.toggleViewAction())

        dock = QDockWidget("Errores", self)
        dock.setAllowedAreas(Qt.BottomDockWidgetArea)
        self.customerList = QListWidget(dock)
        dock.setWidget(self.customerList)
        self.addDockWidget(Qt.BottomDockWidgetArea, dock)
        self.viewMenu.addAction(dock.toggleViewAction())

        dock = QDockWidget("Código objeto", self)
        #dock.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)
        self.customerList = QListWidget(dock)
        dock.setWidget(self.customerList)
        self.addDockWidget(Qt.LeftDockWidgetArea, dock)
        self.viewMenu.addAction(dock.toggleViewAction())