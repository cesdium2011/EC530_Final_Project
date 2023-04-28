import unittest
import os
from app import app
from doc_feed_analyzer import analyze_document, analyze_feed

class TestApp(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()

    def test_upload_file(self):
        with open('test.pdf', 'rb') as f:
            response = self.app.post('/upload_file', data={'file': f}, content_type='multipart/form-data')
            self.assertEqual(response.status_code, 200)

    def test_analyze_document(self):
        test_file_path = 'test.pdf'
        analysis_result = analyze_document(test_file_path)

        self.assertIsNotNone(analysis_result)
        self.assertIn('num_pages', analysis_result)
        self.assertIn('text', analysis_result)

    def test_analyze_feed(self):
        test_file_path = 'test.xml'
        analysis_result = analyze_feed(test_file_path)

        self.assertIsNotNone(analysis_result)
        self.assertIn('num_entries', analysis_result)
        self.assertIn('titles', analysis_result)
        self.assertIn('links', analysis_result)

if __name__ == '__main__':
    unittest.main()
