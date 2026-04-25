import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QLineEdit, QToolBar,
    QAction, QPushButton, QMenu
)
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl


class Browser(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Katia Smart Browser")

        self.browser = QWebEngineView()
        self.browser.setUrl(QUrl("https://www.google.com"))
        self.setCentralWidget(self.browser)

        self.showMaximized()

        # Simulated login state
        self.logged_in = False
        self.username = "User"

        # Toolbar
        navbar = QToolBar()
        navbar.setStyleSheet("background: #202124; padding: 6px; color: white;")
        self.addToolBar(navbar)

        # Back
        back_btn = QAction("⬅️", self)
        back_btn.triggered.connect(self.browser.back)
        navbar.addAction(back_btn)

        # Forward (FIXED ➡️)
        forward_btn = QAction("➡️", self)
        forward_btn.triggered.connect(self.browser.forward)
        navbar.addAction(forward_btn)

        # Reload
        reload_btn = QAction("⟳", self)
        reload_btn.triggered.connect(self.browser.reload)
        navbar.addAction(reload_btn)

        # URL/Search bar
        self.url_bar = QLineEdit()
        self.url_bar.setPlaceholderText("Search Google or type a website...")
        self.url_bar.returnPressed.connect(self.navigate_to_url)
        self.url_bar.setStyleSheet("""
            padding: 8px;
            border-radius: 10px;
            font-size: 14px;
            color: white;
            background-color: #303134;
        """)
        navbar.addWidget(self.url_bar)

        # Account button
        self.account_btn = QPushButton("Login")
        self.account_btn.setStyleSheet("""
            background-color: #8ab4f8;
            color: black;
            padding: 6px 12px;
            border-radius: 8px;
        """)
        self.account_btn.clicked.connect(self.handle_account)
        navbar.addWidget(self.account_btn)

        self.browser.urlChanged.connect(self.update_url)

    def navigate_to_url(self):
        text = self.url_bar.text()

        if "." in text:
            if not text.startswith("http"):
                text = "http://" + text
            url = QUrl(text)
        else:
            url = QUrl(f"https://www.google.com/search?q={text}")

        self.browser.setUrl(url)

    def update_url(self, q):
        self.url_bar.setText(q.toString())

    def handle_account(self):
        if not self.logged_in:
            # Open Google login page
            self.browser.setUrl(QUrl("https://accounts.google.com/signin"))

            # Simulate login success
            self.logged_in = True
            self.username = "GoogleUser"
            self.account_btn.setText(self.username)
        else:
            self.show_account_menu()

    def show_account_menu(self):
        menu = QMenu()

        settings = menu.addAction("Settings (Google)")
        passwords = menu.addAction("Passwords (Google)")
        signout = menu.addAction("Sign Out (Google)")

        action = menu.exec_(self.account_btn.mapToGlobal(self.account_btn.rect().bottomLeft()))

        if action == signout:
            self.logged_in = False
            self.account_btn.setText("Login")


app = QApplication(sys.argv)
QApplication.setApplicationName("Katia Browser")

window = Browser()
app.exec_()