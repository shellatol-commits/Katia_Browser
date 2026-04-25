import sys
import os

os.environ["QTWEBENGINE_CHROMIUM_FLAGS"] = "--disable-gpu"

from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QLineEdit, QToolBar,
    QAction, QMenu, QTabWidget
)
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl, QTimer


app = QApplication(sys.argv)


class KatiaBrowser(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Katia Browser")
        self.resize(1200, 800)

        self.logged_in = False

        self.tabs = QTabWidget()
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self.close_tab)
        self.setCentralWidget(self.tabs)

        navbar = QToolBar()
        self.addToolBar(navbar)

        back_btn = QAction("←", self)
        back_btn.triggered.connect(lambda: self.current_browser().back())
        navbar.addAction(back_btn)

        forward_btn = QAction("→", self)
        forward_btn.triggered.connect(lambda: self.current_browser().forward())
        navbar.addAction(forward_btn)

        reload_btn = QAction("⟳", self)
        reload_btn.triggered.connect(lambda: self.current_browser().reload())
        navbar.addAction(reload_btn)

        new_tab_btn = QAction("+", self)
        new_tab_btn.triggered.connect(self.add_tab)
        navbar.addAction(new_tab_btn)

        self.url_bar = QLineEdit()
        self.url_bar.returnPressed.connect(self.navigate)
        navbar.addWidget(self.url_bar)

        self.login_btn = QAction("Login", self)
        self.login_btn.triggered.connect(self.handle_login)
        navbar.addAction(self.login_btn)

        self.add_tab()

        QTimer.singleShot(1500, self.check_login_state)

    # ---------- Tabs ----------
    def add_tab(self):
        browser = QWebEngineView()
        browser.setUrl(QUrl("https://www.google.com"))

        browser.urlChanged.connect(lambda q, b=browser: self.update_url(q, b))
        browser.urlChanged.connect(self.detect_login)

        self.tabs.addTab(browser, "New Tab")
        self.tabs.setCurrentWidget(browser)

    def close_tab(self, index):
        if self.tabs.count() > 1:
            self.tabs.removeTab(index)

    def current_browser(self):
        return self.tabs.currentWidget()

    # ---------- Navigation ----------
    def navigate(self):
        text = self.url_bar.text().strip()

        if "." not in text:
            text = "https://www.google.com/search?q=" + text
        elif not text.startswith("http"):
            text = "http://" + text

        self.current_browser().setUrl(QUrl(text))

    def update_url(self, q, browser):
        if browser == self.current_browser():
            self.url_bar.setText(q.toString())

    # ---------- 🔥 CORRECT DETECTION ----------
    def detect_login(self, q):
        url = q.toString().lower()

        # LOGGED IN (only strong signal)
        if "myaccount.google.com" in url:
            if not self.logged_in:
                self.logged_in = True
                self.login_btn.setText("User Options")

        # LOGGED OUT (explicit pages only)
        elif (
            "servicelogin" in url or
            "signin" in url or
            "logout" in url
        ):
            if self.logged_in:
                self.logged_in = False
                self.login_btn.setText("Login")

    # ---------- Startup check ----------
    def check_login_state(self):
        browser = self.current_browser()

        browser.setUrl(QUrl("https://myaccount.google.com"))

        QTimer.singleShot(1500, lambda: self.finish_check(browser))

    def finish_check(self, browser):
        url = browser.url().toString().lower()

        if "myaccount.google.com" in url:
            self.logged_in = True
            self.login_btn.setText("User Options")
        else:
            self.logged_in = False
            self.login_btn.setText("Login")

        browser.setUrl(QUrl("https://www.google.com"))

    # ---------- Login ----------
    def handle_login(self):
        if not self.logged_in:
            self.current_browser().setUrl(
                QUrl("https://accounts.google.com/signin")
            )
        else:
            self.show_menu()

    # ---------- Menu ----------
    def show_menu(self):
        menu = QMenu(self)

        settings = menu.addAction("Settings (Google)")
        passwords = menu.addAction("Passwords (Google)")
        signout = menu.addAction("Sign Out")

        action = menu.exec_(self.cursor().pos())

        if action == settings:
            self.current_browser().setUrl(QUrl("https://myaccount.google.com"))

        elif action == passwords:
            self.current_browser().setUrl(QUrl("https://passwords.google.com"))

        elif action == signout:
            self.logout()

    # ---------- Logout ----------
    def logout(self):
        browser = self.current_browser()

        browser.setUrl(QUrl("https://accounts.google.com/logout"))

        self.logged_in = False
        self.login_btn.setText("Login")

        QTimer.singleShot(2000, lambda: browser.setUrl(QUrl("https://www.google.com")))


window = KatiaBrowser()
window.show()

sys.exit(app.exec_())