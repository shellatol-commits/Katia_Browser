import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QLineEdit, QToolBar, QAction, QPushButton
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

        # Toolbar
        navbar = QToolBar()
        navbar.setStyleSheet("background: #2c2f33; padding: 5px;")
        self.addToolBar(navbar)

        # Back button
        back_btn = QAction("⬅", self)
        back_btn.triggered.connect(self.browser.back)
        navbar.addAction(back_btn)

        # Forward button
        forward_btn = QAction("➡", self)
        forward_btn.triggered.connect(self.browser.forward)
        navbar.addAction(forward_btn)

        # Reload button
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
        """)
        navbar.addWidget(self.url_bar)

        # Login button
        login_btn = QPushButton("Login")
        login_btn.setStyleSheet("""
            background-color: #7289da;
            color: white;
            padding: 6px 12px;
            border-radius: 8px;
        """)
        login_btn.clicked.connect(self.login_google)
        navbar.addWidget(login_btn)

        self.browser.urlChanged.connect(self.update_url)

    def navigate_to_url(self):
        text = self.url_bar.text()

        # If it's a URL
        if "." in text:
            if not text.startswith("http"):
                text = "http://" + text
            url = QUrl(text)
        else:
            # Google search fallback
            search_url = f"https://www.google.com/search?q={text}"
            url = QUrl(search_url)

        self.browser.setUrl(url)

    def update_url(self, q):
        self.url_bar.setText(q.toString())

    def login_google(self):
        # Opens Google login page
        self.browser.setUrl(QUrl("https://accounts.google.com/signin"))


app = QApplication(sys.argv)
QApplication.setApplicationName("Katia Browser")

window = Browser()
app.exec_()