import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QLineEdit, QToolBar,
    QAction, QPushButton, QMenu, QWidget, QHBoxLayout
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

        self.logged_in = False
        self.username = "User"

        # Toolbar (FORCE WHITE TEXT)
        navbar = QToolBar()
        navbar.setStyleSheet("""
            background: #202124;
            padding: 6px;
            color: white;
        """)
        self.addToolBar(navbar)

        # Back
        back_btn = QAction("⬅️", self)
        back_btn.triggered.connect(self.browser.back)
        navbar.addAction(back_btn)

        # Forward (FORCED EMOJI)
        forward_btn = QAction("➡️", self)
        forward_btn.triggered.connect(self.browser.forward)
        navbar.addAction(forward_btn)

        # Reload
        reload_btn = QAction("⟳", self)
        reload_btn.triggered.connect(self.browser.reload)
        navbar.addAction(reload_btn)

        # URL bar (WHITE TEXT)
        self.url_bar = QLineEdit()
        self.url_bar.setPlaceholderText("Search Google or type a website...")
        self.url_bar.returnPressed.connect(self.navigate_to_url)
        self.url_bar.setStyleSheet("""
            padding: 8px;
            border-radius: 10px;
            font-size: 14px;
            color: white;
            background-color: #303134;
            selection-background-color: #8ab4f8;
        """)
        navbar.addWidget(self.url_bar)

        # Account button container
        container = QWidget()
        layout = QHBoxLayout()
        layout.setContentsMargins(5, 0, 5, 0)

        self.account_btn = QPushButton("Login")
        self.account_btn.setStyleSheet("""
            background-color: #8ab4f8;
            color: white;
            padding: 6px 12px;
            border-radius: 8px;
        """)
        self.account_btn.clicked.connect(self.handle_account)

        layout.addWidget(self.account_btn)
        container.setLayout(layout)

        navbar.addWidget(container)

        self.browser.urlChanged.connect(self.update_url)

    def navigate_to_url(self):
        text = self.url_bar.text().strip()

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
            self.browser.setUrl(QUrl("https://accounts.google.com/signin"))
            self.logged_in = True
            self.username = "GoogleUser"
            self.account_btn.setText(self.username)
        else:
            self.show_account_menu()

    def show_account_menu(self):
        menu = QMenu(self)

        # FORCE DARK MENU + WHITE TEXT
        menu.setStyleSheet("""
            QMenu {
                background-color: #202124;
                color: white;
                border: 1px solid #444;
            }
            QMenu::item:selected {
                background-color: #3c4043;
            }
        """)

        settings = menu.addAction("Settings (Google)")
        passwords = menu.addAction("Passwords (Google)")
        signout = menu.addAction("Sign Out")

        action = menu.exec(self.account_btn.mapToGlobal(self.account_btn.rect().bottomLeft()))

        if action == settings:
            self.browser.setUrl(QUrl("https://myaccount.google.com/"))

        elif action == passwords:
            self.browser.setUrl(QUrl("https://passwords.google.com/"))

        elif action == signout:
            self.sign_out()

    def sign_out(self):
        self.browser.setUrl(QUrl("https://accounts.google.com/logout"))
        self.logged_in = False
        self.account_btn.setText("Login")


app = QApplication(sys.argv)
QApplication.setApplicationName("Katia Browser")

window = Browser()
app.exec_()