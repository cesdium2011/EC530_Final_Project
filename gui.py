import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QLineEdit, QFileDialog
from doc_feed_analyzer import analyze_document, analyze_feed

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Document and Feed Analyzer")

        layout = QVBoxLayout()

        self.upload_button = QPushButton("Upload PDF File")
        self.upload_button.clicked.connect(self.upload_pdf)
        layout.addWidget(self.upload_button)

        self.feed_input = QLineEdit()
        layout.addWidget(QLabel("Feed URL:"))
        layout.addWidget(self.feed_input)

        self.analyze_button = QPushButton("Analyze")
        self.analyze_button.clicked.connect(self.analyze)
        layout.addWidget(self.analyze_button)

        self.setLayout(layout)

    def upload_pdf(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "Open PDF File", "", "PDF Files (*.pdf)", options=options)
        if file_name:
            self.pdf_file = file_name

    def analyze(self):
        if hasattr(self, "pdf_file"):
            document_analysis = analyze_document(self.pdf_file)
            print("Document Analysis:")
            print(document_analysis)

        feed_url = self.feed_input.text()
        if feed_url:
            feed_analysis = analyze_feed(feed_url)
            print("Feed Analysis:")
            print(feed_analysis)

def main():
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
