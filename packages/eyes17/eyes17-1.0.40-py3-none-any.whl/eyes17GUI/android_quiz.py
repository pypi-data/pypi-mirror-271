'''
Code for viewing quiz via UDP
Logs data from various sensors.
Author  : Jithin B.P, jithinbp@gmail.com
Date    : Sep-2019
License : GNU GPL version 3
'''
import sys, struct
from PyQt5 import QtGui, QtCore, QtWidgets
import os.path, socket

from .layouts import texteditor

from .layouts import ui_android_quiz, ui_quiz_row

class QUIZROW(QtWidgets.QWidget, ui_quiz_row.Ui_Form):
    def __init__(self, parent, address, name, score, result):
        super(QUIZROW, self).__init__(parent)
        self.setupUi(self)
        self.setToolTip('IP:'+address)
        self.nameLabel.setText(name)
        self.scoreLabel.setText(score)
        self.resultLabel.setText(result)

class Expt(QtWidgets.QWidget, ui_android_quiz.Ui_Form):
    p = None
    logThis = QtCore.pyqtSignal(str)
    showStatusSignal = QtCore.pyqtSignal(str, bool)
    serverSignal = QtCore.pyqtSignal(str,str)
    logThisPlain = QtCore.pyqtSignal(bytes)
    codeOutput = QtCore.pyqtSignal(str, str)
    def __init__(self, device=None):
        QtWidgets.QWidget.__init__(self)
        self.setupUi(self)
        self.local_ip = ''

        self.fs_watcher = None
        self.reloadFrame.setVisible(False)

        self.CFile = None  # '~/kuttyPy.c'
        self.defaultDirectory = '.'
        # Define some keyboard shortcuts for ease of use

        ####### C CODE EDITOR #########
        self.codingTabs.tabCloseRequested.connect(self.closeCTab)
        self.codingTabs.tabBarClicked.connect(self.CTabChanged)

        self.activeEditor = None
        self.activeSourceTab = None
        self.sourceTabs = {}
        self.addSourceTab()

        self.addFileMenu()
        self.addEditMenu()

        self.editorFont = QtGui.QFont()
        self.editorFont.setPointSize(12)
        self.editorFont.setFamily('Ubuntu mono')

        self.MCAST_GRP = '234.0.0.2'
        self.MCAST_PORT = 9999
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)

        self.sock.setsockopt(socket.SOL_IP, socket.IP_MULTICAST_TTL, struct.pack('b', 5))
        self.sock.setsockopt(socket.SOL_IP, socket.SO_REUSEADDR, 1)
        self.sock.setsockopt(socket.SOL_IP, socket.IP_MULTICAST_LOOP, 1)

        # self.sock.bind(("10.42.0.1", self.MCAST_PORT))
        self.sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 32)
        self.serverSignal.connect(self.registerResponse)

        self.responses = {}  # List of responses
        self.activateQuizListener()

        self.MAX_COLUMNS = 4
        self.response_row=0
        self.response_column=0

        for a in range(20):
            row = QUIZROW(self,'hi'+str(a),'----', '---', '--------')
            self.responsesLayout.addWidget(row,self.response_row,self.response_column)
            self.responses[id] = row
            self.response_column+=1
            if self.response_column>self.MAX_COLUMNS:
                self.response_column = 0
                self.response_row+=1

        global app

    def closeEvent(self, event):
        self.external.terminate()
        self.external.waitForFinished(1000)

    def close_maybe(self):
        print('terminal closed')

    def registerResponse(self, addr, msg):
        print(addr,msg)
        if addr == 'ERROR':
            self.termFrame.setStyleSheet('background: #f00;')
            l = QtWidgets.QLabel(msg)
            self.responsesLayout.addWidget(l)
            return
        name,res = msg.split(':')
        score, responses = res.split('\t')
        id=addr+name
        if id not in self.responses:
            row = QUIZROW(self,addr,name, score, responses)
            self.responsesLayout.addWidget(row,self.response_row,self.response_column)
            self.responses[id] = row
            self.response_column+=1
            if self.response_column>self.MAX_COLUMNS:
                self.response_column = 0
                self.response_row+=1

        else:
            row = self.responses[id]
            row.scoreLabel.setText(score)
            row.resultLabel.setText(responses)
    def activateQuizListener(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.settimeout(0.1)  # Set a timeout to avoid blocking indefinitely
        s.connect(("8.8.8.8", 80))  # Connect to a public IP address
        self.local_ip = s.getsockname()[0]

        from .layouts.quiz_server import create_server
        self.quiz_thread = create_server(self.showStatusSignal, self.serverSignal, self.local_ip)
        self.showStatusSignal.connect(self.showStatus)
        s.close()

    def addFileMenu(self):
        codeMenu = QtWidgets.QMenu()

        newFileAction = QtWidgets.QAction('New File', self)
        newFileAction.setShortcut(QtGui.QKeySequence("Ctrl+N"))
        ico = QtGui.QIcon()
        ico.addPixmap(QtGui.QPixmap(":/control/plus.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        newFileAction.setIcon(ico)
        newFileAction.triggered.connect(self.addSourceTab)
        codeMenu.addAction(newFileAction)

        openFileAction = QtWidgets.QAction('Open File', self)
        openFileAction.setShortcut(QtGui.QKeySequence("Ctrl+O"))
        openFileAction.triggered.connect(self.openFile)
        openIcon = QtGui.QIcon()
        openIcon.addPixmap(QtGui.QPixmap(":/control/document-open.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        openFileAction.setIcon(openIcon)
        codeMenu.addAction(openFileAction)

        saveFileAction = QtWidgets.QAction('Save File', self)
        saveFileAction.setShortcut(QtGui.QKeySequence("Ctrl+S"))
        saveFileAction.triggered.connect(self.saveFile)
        saveIcon = QtGui.QIcon()
        saveIcon.addPixmap(QtGui.QPixmap(":/control/saveall.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        saveFileAction.setIcon(saveIcon)
        codeMenu.addAction(saveFileAction)

        saveAsFileAction = QtWidgets.QAction('Save As', self)
        saveAsFileAction.setShortcut(QtGui.QKeySequence("Ctrl+Shift+S"))
        saveAsFileAction.triggered.connect(self.saveAs)
        saveAsFileAction.setIcon(saveIcon)
        codeMenu.addAction(saveAsFileAction)

        exitAction = QtWidgets.QAction('Exit', self)
        exitAction.triggered.connect(QtWidgets.qApp.quit)
        codeMenu.addAction(exitAction)
        self.fileMenuButton.setMenu(codeMenu)

    def closeEvent(self, evnt):
        evnt.ignore()
        self.askBeforeQuit()

    def askBeforeQuit(self):
        ask = False
        for editors in self.sourceTabs:
            if self.sourceTabs[editors][0].changed:
                ask = True
        if ask:
            reply = QtWidgets.QMessageBox.question(self, 'Warning', 'Files may have unsaved changes.\nReally quit?',
                                                   QtWidgets.QMessageBox.Yes, QtWidgets.QMessageBox.No)
            if reply == QtWidgets.QMessageBox.No:
                return

        self.userHexRunning = False
        global app
        app.quit()

    def addEditMenu(self):
        codeMenu = QtWidgets.QMenu()

        undoAction = QtWidgets.QAction('Undo', self)
        undoAction.setShortcut(QtGui.QKeySequence("Ctrl+Z"))
        undoAction.triggered.connect(self.activeEditor.undo)
        ico = QtGui.QIcon()
        ico.addPixmap(QtGui.QPixmap(":/control/reset.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        undoAction.setIcon(ico)
        codeMenu.addAction(undoAction)

        redoAction = QtWidgets.QAction('Redo', self)
        redoAction.setShortcut(QtGui.QKeySequence("Ctrl+Shift+Z"))
        redoAction.triggered.connect(self.activeEditor.redo)
        codeMenu.addAction(redoAction)
        a = QtWidgets.QAction('Cut', self)
        a.setShortcut(QtGui.QKeySequence("Ctrl+X"))
        a.triggered.connect(self.activeEditor.cut)
        codeMenu.addAction(a)
        a = QtWidgets.QAction('Copy', self)
        a.setShortcut(QtGui.QKeySequence("Ctrl+C"))
        a.triggered.connect(self.activeEditor.copy)
        codeMenu.addAction(a)
        a = QtWidgets.QAction('Paste', self)
        a.setShortcut(QtGui.QKeySequence("Ctrl+V"))
        a.triggered.connect(self.activeEditor.paste)
        codeMenu.addAction(a)
        a = QtWidgets.QAction('Select All', self)
        a.setShortcut(QtGui.QKeySequence("Ctrl+A"))
        a.triggered.connect(self.activeEditor.selectAll)
        codeMenu.addAction(a)

        self.editMenuButton.setMenu(codeMenu)

    def closeCTab(self, index):
        print('Close Tab', index)
        widget = self.codingTabs.widget(index)
        sourceTabClosed = False
        if len(self.sourceTabs) == 1:
            print("last tab. won't close.")
            return
        else:
            print('closing source tab', widget.objectName())
            self.sourceTabs.pop(widget)
            sourceTabClosed = True

        self.codingTabs.removeTab(index)
        if sourceTabClosed:  # Source Tab closed. Re-assign active source tab
            self.activeSourceTab = list(self.sourceTabs.keys())[0]
            self.activeEditor = self.sourceTabs[self.activeSourceTab][0]
            self.CFile = self.sourceTabs[self.activeSourceTab][1]
            self.codingTabs.setCurrentIndex(self.codingTabs.indexOf(self.activeSourceTab))
            print('New Source Tab:', self.getActiveFilename(), self.CFile)

    def getActiveFilename(self):
        self.codingTabs.tabText(self.codingTabs.indexOf(self.activeSourceTab))

    def addSourceTab(self):
        sourceTab = QtWidgets.QWidget()
        sourceTab.setObjectName("sourceTab")
        horizontalLayout_3 = QtWidgets.QHBoxLayout(sourceTab)
        horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        horizontalLayout_3.setSpacing(0)
        horizontalLayout_3.setObjectName("horizontalLayout_3")
        editor = texteditor.myTextEditor(sourceTab, self.codingTabs)
        font = QtGui.QFont()
        font.setFamily("Ubuntu Mono")
        font.setPointSize(12)
        editor.setFont(font)
        editor.setObjectName("editor")
        editor.setTabChangesFocus(False)
        horizontalLayout_3.addWidget(editor)
        self.codingTabs.addTab(sourceTab, "")
        self.sourceTabs[sourceTab] = [editor, None]
        self.codingTabs.setCurrentIndex(self.codingTabs.indexOf(sourceTab))
        self.codingTabs.setTabText(self.codingTabs.indexOf(sourceTab), 'Untitled')
        self.CFile = None
        self.activeSourceTab = sourceTab
        self.activeEditor = editor

    def CTabChanged(self, index):
        widget = self.codingTabs.widget(index)
        if widget in self.sourceTabs:
            self.activeSourceTab = widget
            self.activeEditor = self.sourceTabs[widget][0]
            self.CFile = self.sourceTabs[widget][1]
            print('Change Tab', index, self.codingTabs.tabText(index), self.CFile)

    def openFile(self):
        filename = QtWidgets.QFileDialog.getOpenFileName(self, " Open a text file to edit", self.defaultDirectory,
                                                         "Text Files (*.txt *.TXT)")
        if len(filename[0]):
            self.openFile_(filename[0])

    def openFile_(self, fname):
        for sourceTab in self.sourceTabs:
            print(self.sourceTabs[sourceTab][1], fname)
            if fname == self.sourceTabs[sourceTab][1]:  # File is already open
                self.activeSourceTab = sourceTab
                self.activeEditor = self.sourceTabs[sourceTab][0]
                self.CFile = self.sourceTabs[sourceTab][1]
                self.codingTabs.setCurrentIndex(self.codingTabs.indexOf(sourceTab))
                return

        if self.CFile is not None:  # A file is altready open
            self.addSourceTab()
        # self.defaultDirectory = ''
        self.CFile = fname
        self.defaultDirectory = os.path.split(self.CFile)[0]
        self.sourceTabs[self.activeSourceTab][1] = self.CFile
        infile = open(fname, 'r')
        self.activeEditor.setPlainText(
            infile.read())  # self.activeEditor = self.sourceTabs[self.activeSourceTab][0]
        infile.close()
        self.codingTabs.setTabText(self.codingTabs.indexOf(self.activeSourceTab), os.path.split(self.CFile)[1])
        filetype = 'c'
        if self.CFile.endswith('.S') or self.CFile.endswith('.s'):
            filetype = 'asm'
        ico = QtGui.QIcon()
        ico.addPixmap(QtGui.QPixmap(f":/control/{filetype}.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.codingTabs.setTabIcon(self.codingTabs.indexOf(self.activeSourceTab), ico)
        self.updateWatcher()

    def updateWatcher(self):
        paths = []
        for sourceTab in self.sourceTabs:
            paths.append(self.sourceTabs[sourceTab][1])
        self.fs_watcher = QtCore.QFileSystemWatcher(paths)
        self.fs_watcher.fileChanged.connect(self.file_changed)
        print('updated watcher', paths)

    def file_changed(self, path):
        print('File Changed: %s' % path)
        self.reloadLabel.setText(path)
        self.reloadFrame.setVisible(True)

    def reloadFile(self):
        self.reloadFrame.setVisible(False)
        fname = self.reloadLabel.text()
        for sourceTab in self.sourceTabs:
            print(self.sourceTabs[sourceTab][1], fname)
            if fname == self.sourceTabs[sourceTab][1]:  # File is already open
                self.activeSourceTab = sourceTab
                self.activeEditor = self.sourceTabs[sourceTab][0]
                self.CFile = self.sourceTabs[sourceTab][1]
                self.codingTabs.setCurrentIndex(self.codingTabs.indexOf(sourceTab))
                self.defaultDirectory = os.path.split(self.CFile)[0]

                infile = open(fname, 'r')
                self.activeEditor.setPlainText(
                    infile.read())  # self.activeEditor = self.sourceTabs[self.activeSourceTab][0]
                infile.close()
                filetype = 'c'
                if self.CFile.endswith('.S') or self.CFile.endswith('.s'):
                    filetype = 'asm'
                ico = QtGui.QIcon()
                ico.addPixmap(QtGui.QPixmap(f":/control/{filetype}.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
                self.codingTabs.setTabIcon(self.codingTabs.indexOf(self.activeSourceTab), ico)
                self.updateWatcher()
                return
        print(' Modified file is not open anymore', fname)

    def cancelReload(self):
        self.reloadFrame.setVisible(False)
        self.updateWatcher()

    def upload(self):
        print('upload')
        for a in self.responses:
            self.responsesLayout.removeWidget(self.responses[a])
            self.responses[a].setParent(None)
        self.responses = {}
        self.response_row=0
        self.response_column=0
        dat = self.activeEditor.toPlainText().encode('utf-8')
        self.sock.sendto(dat, (self.MCAST_GRP, self.MCAST_PORT))

    def saveFile(self):
        if not self.CFile:
            self.CFile = self.saveAs()
        if self.CFile is not None and len(self.CFile) > 1:
            self.sourceTabs[self.activeSourceTab][1] = self.CFile
            self.activeEditor.markAsSaved(True)
            self.fs_watcher.removePath(self.CFile)
            fn = open(self.CFile, 'w')
            fn.write(self.activeEditor.toPlainText())
            fn.close()
            self.fs_watcher.addPath(self.CFile)
            self.codingTabs.setTabText(self.codingTabs.indexOf(self.activeSourceTab), os.path.split(self.CFile)[1])

    def saveAs(self):
        name = QtWidgets.QFileDialog.getSaveFileName(self, 'Save File')
        print('created new file:', name)
        if len(name) > 0 and len(name[0]) > 1:
            self.CFile = name[0]
            self.codingTabs.setTabText(self.codingTabs.indexOf(self.activeSourceTab), os.path.split(self.CFile)[1])
            self.saveFile()
            return self.CFile


    def showStatus(self, msg, error=None):
        print(msg,error)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    # translation stuff
    lang = QtCore.QLocale.system().name()
    t = QtCore.QTranslator()
    t.load("lang/" + lang, os.path.dirname(__file__))
    app.installTranslator(t)
    t1 = QtCore.QTranslator()
    t1.load("qt_" + lang,
            QtCore.QLibraryInfo.location(QtCore.QLibraryInfo.TranslationsPath))
    app.installTranslator(t1)

    mw = Expt(None)
    mw.show()
    sys.exit(app.exec_())
