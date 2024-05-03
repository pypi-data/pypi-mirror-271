#!/usr/bin/env python3
# shamelessly copy/pasted from https://stackoverflow.com/a/12712362

from typing import List

from PySide2 import QtCore
from PySide2.QtCore import QCoreApplication, QEventLoop, Qt, QTextStream
from PySide2.QtNetwork import QLocalServer, QLocalSocket
from PySide2.QtWidgets import QApplication, QMainWindow

# from https://github.com/qutebrowser/qutebrowser/blob/c073412b49002ff75bf67fac1c3e59560135a51b/qutebrowser/mainwindow/mainwindow.py#L70


def raise_window(window: QMainWindow):
    """Raise the given MainWindow object."""
    window.setWindowState(
        window.windowState() & ~Qt.WindowState.WindowMinimized
    )
    window.setWindowState(window.windowState() | Qt.WindowState.WindowActive)
    window.raise_()
    # WORKAROUND for https://bugreports.qt.io/browse/QTBUG-69568
    QCoreApplication.processEvents(
        QEventLoop.ProcessEventsFlag.ExcludeUserInputEvents
        | QEventLoop.ProcessEventsFlag.ExcludeSocketNotifiers
    )

    # if sip.isdeleted(window):
    # Could be deleted by the events run above
    #   return

    window.activateWindow()


class QtSingleApplication(QApplication):

    messageReceived = QtCore.Signal()

    def __init__(self, id: str, args: List[str]):
        super().__init__(args)
        self._id = id
        self._activationWindow: QMainWindow = None
        self._activateOnMessage = False

        # Is there another instance running?
        self._outSocket = QLocalSocket()
        self._outSocket.connectToServer(self._id)
        self._isRunning = self._outSocket.waitForConnected()

        if self._isRunning:
            # Yes, there is.
            self._outStream = QTextStream(self._outSocket)
            self._outStream.setCodec("UTF-8")
        else:
            # No, there isn't.
            self._outSocket = None
            self._outStream = None
            self._inSocket = None
            self._inStream = None
            self._server = QLocalServer()
            self._server.listen(self._id)
            self._server.newConnection.connect(self._onNewConnection)

    def isRunning(self):
        return self._isRunning

    def id(self):
        return self._id

    def activationWindow(self):
        return self._activationWindow

    def setActivationWindow(
        self, activationWindow: QMainWindow, activateOnMessage=True
    ):
        self._activationWindow = activationWindow
        self._activateOnMessage = activateOnMessage

    def activateWindow(self):
        if not self._activationWindow:
            return
        raise_window(self._activationWindow)

    def sendMessage(self, msg):
        if not self._outStream:
            return False
        self._outStream << msg << "\n"
        self._outStream.flush()
        return self._outSocket.waitForBytesWritten()

    def _onNewConnection(self):
        if self._inSocket:
            self._inSocket.readyRead.disconnect(self._onReadyRead)
        self._inSocket = self._server.nextPendingConnection()
        if not self._inSocket:
            return
        self._inStream = QTextStream(self._inSocket)
        self._inStream.setCodec("UTF-8")
        self._inSocket.readyRead.connect(self._onReadyRead)
        if self._activateOnMessage:
            self.activateWindow()

    def _onReadyRead(self):
        while True:
            msg = self._inStream.readLine()
            if not msg:
                break
            self.messageReceived.emit(msg)
