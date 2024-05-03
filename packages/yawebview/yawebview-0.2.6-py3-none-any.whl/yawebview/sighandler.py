import signal
import socket

from PySide2 import QtCore
from PySide2.QtNetwork import QAbstractSocket
from PySide2.QtWidgets import QApplication

# from https://stackoverflow.com/a/37229299


class SignalWakeupHandler(QAbstractSocket):
    def __init__(self, parent=None):
        super().__init__(QAbstractSocket.UdpSocket, parent)
        self.old_fd = None
        # Create a socket pair
        self.wsock, self.rsock = socket.socketpair(type=socket.SOCK_DGRAM)
        # Let Qt listen on the one end
        self.setSocketDescriptor(self.rsock.fileno())
        # And let Python write on the other end
        self.wsock.setblocking(False)
        self.old_fd = signal.set_wakeup_fd(self.wsock.fileno())
        # First Python code executed gets any exception from
        # the signal handler, so add a dummy handler first
        self.readyRead.connect(lambda: None)
        # Second handler does the real handling
        self.readyRead.connect(self._readSignal)

    def __del__(self):
        # Restore any old handler on deletion
        if self.old_fd is not None and signal and signal.set_wakeup_fd:
            signal.set_wakeup_fd(self.old_fd)

    def _readSignal(self):
        # Read the written byte.
        # Note: readyRead is blocked from occuring again until readData()
        # was called, so call it, even if you don't need the value.
        data = self.readData(1)
        # Emit a Qt signal for convenience
        self.signalReceived.emit(data[0])

    signalReceived = QtCore.Signal(int)


def set_termination_signals_handler(signal_handler):
    # Handle termination signals to ensure clean exit
    # even if the process crashes
    signal.signal(signal.SIGHUP, signal_handler)  # 1
    signal.signal(signal.SIGINT, signal_handler)  # 2
    signal.signal(signal.SIGQUIT, signal_handler)  # 3
    signal.signal(signal.SIGILL, signal_handler)  # 4
    signal.signal(signal.SIGABRT, signal_handler)  # 6
    signal.signal(signal.SIGFPE, signal_handler)  # 8
    signal.signal(signal.SIGBUS, signal_handler)  # 10
    signal.signal(signal.SIGSEGV, signal_handler)  # 11
    signal.signal(signal.SIGSYS, signal_handler)  # 12
    signal.signal(signal.SIGPIPE, signal_handler)  # 13
    signal.signal(signal.SIGALRM, signal_handler)  # 14
    signal.signal(signal.SIGTERM, signal_handler)  # 15
    signal.signal(signal.SIGXCPU, signal_handler)  # 24
    signal.signal(signal.SIGXFSZ, signal_handler)  # 25


def crash_handler(app: QApplication):
    SignalWakeupHandler(app)
    set_termination_signals_handler(
        lambda signum, _: QtCore.QTimer.singleShot(10, app.quit)
    )
