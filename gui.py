import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QFileDialog, QPlainTextEdit, QListWidget

class AppDemo(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('File Upload and Feed Ingestion App')
        self.resize(400, 300)

        layout = QVBoxLayout()

        # File upload section
        file_upload_label = QLabel('Upload a file:')
        layout.addWidget(file_upload_label)

        self.file_upload_btn = QPushButton('Select a file')
        self.file_upload_btn.clicked.connect(self.select_file)
        layout.addWidget(self.file_upload_btn)

        self.uploaded_files_list = QListWidget()
        self.uploaded_files_list.setFixedHeight(100)
        layout.addWidget(self.uploaded_files_list)

        # Feed ingestion section
        feed_ingestion_label = QLabel('Ingest a feed:')
        layout.addWidget(feed_ingestion_label)

        self.feed_url_input = QPlainTextEdit()
        self.feed_url_input.setFixedHeight(50)
        layout.addWidget(self.feed_url_input)

        self.ingest_feed_btn = QPushButton('Ingest feed')
        self.ingest_feed_btn.clicked.connect(self.ingest_feed)
        layout.addWidget(self.ingest_feed_btn)

        self.ingest_feed_status = QLabel()
        layout.addWidget(self.ingest_feed_status)

        self.setLayout(layout)

    def select_file(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        file_name, _ = QFileDialog.getOpenFileName(self, 'Select a file', '', 'All Files (*);;Text Files (*.txt)', options=options)

        if file_name:
            self.uploaded_files_list.addItem(file_name)
            # Implement file uploading logic here

    def ingest_feed(self):
        feed_url = self.feed_url_input.toPlainText().strip()
        if feed_url:
            # Implement feed ingestion logic here
            self.ingest_feed_status.setText(f"Ingested feed: {feed_url}")
        else:
            self.ingest_feed_status.setText("Please enter a feed URL.")

app = QApplication(sys.argv)
demo = AppDemo()
demo.show()
sys.exit(app.exec_())
