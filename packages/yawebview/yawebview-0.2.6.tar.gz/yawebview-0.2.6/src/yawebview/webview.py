import logging
import sys
from dataclasses import dataclass
from typing import Dict, List, Optional

from PySide2.QtCore import (
    QDir,
    QEvent,
    QIODevice,
    QSizeF,
    Qt,
    QTemporaryFile,
    QUrl,
)
from PySide2.QtGui import (
    QGuiApplication,
    QIcon,
    QKeyEvent,
    QKeySequence,
    QPixmap,
)
from PySide2.QtWebEngineWidgets import (
    QWebEnginePage,
    QWebEngineProfile,
    QWebEngineSettings,
    QWebEngineView,
)
from PySide2.QtWidgets import QApplication, QMainWindow, QShortcut, QWidget

from yawebview import sighandler
from yawebview.QtSingleApplication import QtSingleApplication


@dataclass
class Options:
    user_agent: Optional[str] = None
    single_instance_mode: bool = False
    app_id: str = ""


class Window:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Window, cls).__new__(cls)
        return cls._instance

    def __init__(
        self,
        title: str,
        url: str,
        scrollbars: bool = True,
        context_menu: bool = True,
        title_from_page: bool = True,
        allow_scripts_to_close: bool = False,
        freeze_on_focus_loss: bool = False,  # WIP
    ):
        self.title = title
        self.url = url
        self.show_scrollbars = scrollbars
        self.disable_context_menu = not context_menu
        self.set_title_from_page = title_from_page
        # self.width =
        # self.height
        self.allow_scripts_to_close = allow_scripts_to_close
        self._freeze_on_focus_loss = freeze_on_focus_loss
        self.icon_set = False
        self.keymappings: Dict[str, str] = {}

    def set_icon(self, icon_name: str, fallback_icon_files: List[str] = []):
        self.icon_set = True
        self.icon_name = icon_name
        self.fallback_icon_files = fallback_icon_files

    def add_keymapping(self, src_key_sequence: str, dest_key_sequence: str):
        self.keymappings[src_key_sequence] = dest_key_sequence


class WebEnginePage(QWebEnginePage):
    WINDOW_CLOSE_ERROR = (
        "Scripts may close only the windows that were opened by "
    )

    def __init__(self, profile, parent=None):
        super().__init__(profile, parent)

    def javaScriptConsoleMessage(self, level, message, lineNumber, sourceID):
        if (
            level
            == QWebEnginePage.JavaScriptConsoleMessageLevel.WarningMessageLevel
        ) and WebEnginePage.WINDOW_CLOSE_ERROR.casefold() in message.casefold():
            self.windowCloseRequested.emit()
            return

        if (
            level
            == QWebEnginePage.JavaScriptConsoleMessageLevel.InfoMessageLevel
        ):
            logging.info(f"js: {message}")
        elif (
            level
            == QWebEnginePage.JavaScriptConsoleMessageLevel.WarningMessageLevel
        ):
            logging.warn(f"js: {message}")
        else:  # QWebEnginePage.JavaScriptConsoleMessageLevel.ErrorMessageLevel
            logging.error(f"js: {message}")


class BrowserView(QMainWindow):
    def __init__(self, window: Window, user_agent: Optional[str] = None):
        super().__init__()
        self._freeze_on_focus_loss = window._freeze_on_focus_loss
        self.initUI(window=window, user_agent=user_agent)

    def initUI(self, window: Window, user_agent: Optional[str]):
        for src_seq in window.keymappings.keys():
            src_q_key_seq = QKeySequence(src_seq)
            if src_q_key_seq.toString() == "":
                logging.warning(f"Invalid key sequence '{src_seq}'")
                continue
            dest_seq = window.keymappings[src_seq]
            dest_q_key_seq = QKeySequence(dest_seq)
            if dest_q_key_seq.toString() == "":
                logging.warning(f"Invalid key sequence '{dest_seq}'")
                continue
            shortcut = QShortcut(src_q_key_seq, self)
            # Hacky solution, but works for my requirements
            shortcut.activated.connect(
                lambda: self.fake_key_press(dest_q_key_seq[0])
            )

        self.webEngineView = QWebEngineView(self)
        profile = QWebEngineProfile.defaultProfile()
        if user_agent:
            profile.setHttpUserAgent(user_agent)
        self.page = WebEnginePage(profile=profile, parent=self.webEngineView)
        if window.set_title_from_page:
            self.page.titleChanged.connect(self.setWindowTitle)
        if window.allow_scripts_to_close:
            self.page.windowCloseRequested.connect(self.close)
        self.webEngineView.setPage(self.page)
        if self._freeze_on_focus_loss:
            self.tempFile = QTemporaryFile(
                QDir.tempPath() + QDir.separator() + "yttv_XXXXXX.png",
                parent=self,
            )
            self.tempPage: QWebEnginePage = QWebEnginePage(profile)

        self.webEngineView.settings().setAttribute(
            QWebEngineSettings.ShowScrollBars, window.show_scrollbars
        )
        if window.disable_context_menu:
            self.webEngineView.setContextMenuPolicy(Qt.NoContextMenu)

        self.webEngineView.setUrl(QUrl(window.url))
        self.setCentralWidget(self.webEngineView)

        self.setWindowTitle(window.title)
        if window.icon_set:
            self.set_icon(window.icon_name, window.fallback_icon_files)
        self.resize(
            QGuiApplication.primaryScreen().availableGeometry().size() * 0.7
        )
        self.center()

    def event(self, event: QEvent) -> bool:
        # page switching hack is used since disabling page was not working
        # and WebEngine Lifecycle state wont work on forground page
        if (
            self._freeze_on_focus_loss
            and event.type() == QEvent.WindowActivate
        ):
            # Page Lifecycle API is supported only on Qt 5.14.0 or above
            self.page.setLifecycleState(QWebEnginePage.LifecycleState.Active) 
            self.webEngineView.setPage(self.page)
            self.tempPage.setLifecycleState(QWebEnginePage.LifecycleState.Discarded)
        elif (
            self._freeze_on_focus_loss
            and event.type() == QEvent.WindowDeactivate
        ):
            content_dimensions: QSizeF = self.page.contentsSize()
            width, height = (
                content_dimensions.width(),
                content_dimensions.height(),
            )
            pixmap = QPixmap(int(width), int(height))
            v: QWidget = self.page.view()
            v.render(pixmap)

            self.tempFile.open(QIODevice.WriteOnly)
            pixmap.save(self.tempFile)
            self.tempFile.close()

            self.tempPage.setUrl(QUrl.fromLocalFile(self.tempFile.fileName()))
            self.tempPage.setLifecycleState(QWebEnginePage.LifecycleState.Active)
            self.webEngineView.setPage(self.tempPage)
            # Page Lifecycle API is supported only on Qt 5.14.0 or above
            self.page.setLifecycleState(QWebEnginePage.LifecycleState.Frozen) 
        return super().event(event)

    # shamelessly copy/pasted from qute browser
    def fake_key_press(
        self,
        key: Qt.Key,
        modifier: Qt.KeyboardModifier = Qt.KeyboardModifier.NoModifier,
    ) -> None:
        """Send a fake key event."""
        press_evt = QKeyEvent(QEvent.Type.KeyPress, key, modifier, 0, 0, 0)
        release_evt = QKeyEvent(QEvent.Type.KeyRelease, key, modifier, 0, 0, 0)
        self.send_event(press_evt)
        self.send_event(release_evt)

    def send_event(self, evt: QEvent) -> None:
        """Send the given event to the underlying widget.

        The event will be sent via QApplication.postEvent.
        Note that a posted event must not be re-used in any way!
        """
        # This only gives us some mild protection against re-using events, but
        # it's certainly better than a segfault.
        if getattr(evt, "posted", False):
            logging.error("Can't re-use an event which was already " "posted!")
            return

        recipient = self.webEngineView.focusProxy()
        evt.posted = True  # type: ignore[attr-defined]
        QApplication.postEvent(recipient, evt)

    def center(self):
        qr = self.frameGeometry()
        cp = QGuiApplication.primaryScreen().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def set_icon(self, icon_name, fallback_icon_files):
        fallback_icon = QIcon()
        for filename in fallback_icon_files:
            pixmap = QPixmap()
            pixmap.load(filename)
            if pixmap.isNull():
                logging.warning(f"Failed to load {filename}")
            else:
                fallback_icon.addPixmap(pixmap)
        icon = QIcon.fromTheme(icon_name, fallback_icon)
        if icon.isNull():
            logging.warning("Failed to load icon")
        else:
            self.setWindowIcon(icon)


def start(options: Options = Options()):
    args = sys.argv
    args.append("--disable-seccomp-filter-sandbox")
    if options.single_instance_mode:
        id = options.app_id
        if len(id) < 4:
            logging.error("app id length < 4")
            sys.exit(1)
        app = QtSingleApplication(id, args)
        sighandler.crash_handler(app)
        if app.isRunning():
            logging.info("Another instance is already running")
            sys.exit(0)
    else:
        app = QApplication(args)
        sighandler.crash_handler(app)
    w = BrowserView(Window._instance, user_agent=options.user_agent)
    w.show()
    if options.single_instance_mode:
        app.setActivationWindow(w)
    sys.exit(app.exec_())
