import unittest
from flask import Flask
from flask.testing import FlaskClient
from unittest.mock import patch
from io import BytesIO

from app import recognition_blueprint, face_recognition_blueprint


class TestRecognitionEndpoints(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Setup Flask app and register the blueprints
        cls.app = Flask(__name__)
        cls.app.register_blueprint(recognition_blueprint)
        cls.app.register_blueprint(face_recognition_blueprint)
        cls.client = cls.app.test_client()

    # Test the '/recognition' endpoint with valid parameters
    @patch('utils.file_utils.download_file_from_url')
    @patch('controllers.recognizer_controller.ModelRecognitionController.extract_zip')
    @patch('controllers.recognizer_controller.ModelRecognitionController.list_images')
    @patch('controllers.recognizer_controller.ModelRecognitionController.recognize')
    def test_recognition_valid(self, mock_recognize, mock_list_images, mock_extract_zip, mock_download_file):
        mock_download_file.return_value = 'fake_zip_file.zip'
        mock_extract_zip.return_value = '/fake/extracted/folder'
        mock_list_images.return_value = ['/fake/extracted/folder/image1.jpg', '/fake/extracted/folder/image2.jpg']
        mock_recognize.return_value.to_json.return_value = '{"result": "success"}'

        data = {
            "zip_url": "https://drive.google.com/uc?export=download&id=15m-a4lg37vu5jW83GyUzwRQBFTsSedd7",
            "model_type": "face_recognition",
            "confidence_threshold": 0.8,
            "word": "face"
        }

        response = self.client.post('/recognition', json=data, content_type="application/json")

        # Assert response status code and message
        self.assertEqual(response.status_code, 200)
        self.assertIn('ZIP extracted and images listed', response.json['message'])
        self.assertEqual(response.json['results'],[{'result': 'success'}, {'result': 'success'}])

    # Test the '/recognition' endpoint with invalid 'confidence_threshold'
    def test_recognition_invalid_confidence_threshold(self):
        data = {
            'zip_url': 'http://example.com/fake.zip',
            'model_type': 'face_recognition',
            'confidence_threshold': 'invalid',
            'word': 'face'
        }

        # Send POST request
        response = self.client.post('/recognition', json=data)

        # Assert response status code and error message
        self.assertEqual(response.status_code, 400)
        self.assertIn('confidence_threshold must be a valid number', response.json['message'])

    # Test the '/recognition' endpoint with missing 'zip_url'
    def test_recognition_missing_zip_url(self):
        data = {
            'model_type': 'face_recognition',
            'confidence_threshold': 0.8,
            'word': 'face'
        }

        # Send POST request
        response = self.client.post('/recognition', json=data)

        # Assert response status code and error message
        self.assertEqual(response.status_code, 400)
        self.assertIn('zip_url', response.json['message'])

    #TODO: Review the response for code status 200!=400 Expected: 400 Actual: 200
    # Test the '/face_recognition' endpoint with valid parameters and image file
    @patch('utils.file_utils.download_file_from_url')
    @patch('controllers.recognizer_controller.ModelRecognitionController.extract_zip')
    @patch('controllers.recognizer_controller.ModelRecognitionController.list_images')
    @patch('controllers.recognizer_controller.ModelRecognitionController.recognize_face')
    def test_face_recognition_valid(self, mock_recognize_face, mock_list_images, mock_extract_zip, mock_download_file):
        mock_download_file.return_value = 'fake_zip_file.zip'
        mock_extract_zip.return_value = '/fake/extract/folder'
        mock_list_images.return_value = ['/fake/extract/folder/image1.jpg', '/fake/extract/folder/image2.jpg']
        mock_recognize_face.return_value = {'result': 'success'}

        data = {
            'zip_url': 'https://drive.google.com/uc?export=download&id=15m-a4lg37vu5jW83GyUzwRQBFTsSedd7',
            'model_type': 'face_recognition',
            'confidence_threshold': 0.8,
            'word': 'face'
        }

        files = {
            'image_file_reference': (BytesIO(b"fake image content"), 'reference_image.jpg')  # Proper file
        }

        # Send POST request with form data and image
        response = self.client.post('/face_recognition',data={**data, **files}, content_type='multipart/form-data', follow_redirects=True)

        print(response.data)
        print(response.json)
        # Assert response status code and message
        self.assertEqual(response.status_code, 200)
        self.assertIn('ZIP extracted and images listed', response.json['message'])
        self.assertEqual(len(response.json['results']), 2)

        # Test the '/face_recognition' endpoint with missing 'image_file_reference'
    def test_face_recognition_missing_image_file_reference(self):
        data = {
            'zip_url': 'http://example.com/fake.zip',
            'model_type': 'face_recognition',
            'confidence_threshold': 0.8,
            'word': 'face'
        }

        # Send POST request
        response = self.client.post('/face_recognition', data=data, content_type='multipart/form-data')

        # Assert response status code and error message
        self.assertEqual(response.status_code, 400)
        self.assertIn('image_file_reference', response.json['message'])

    # Test the '/face_recognition' endpoint with invalid 'confidence_threshold'
    def test_face_recognition_invalid_confidence_threshold(self):
        data = {
            'zip_url': 'http://example.com/fake.zip',
            'model_type': 'face_recognition',
            'confidence_threshold': 'invalid',
            'word': 'face'
        }

        files = {
            'image_file_reference': (BytesIO(b"fake image content"), 'reference_image.jpg')
        }

        # Send POST request with invalid confidence_threshold
        response = self.client.post('/face_recognition', data=data, content_type='multipart/form-data', follow_redirects=True)

        # Assert response status code and error message
        self.assertEqual(response.status_code, 400)
        self.assertIn('confidence_threshold must be a valid number', response.json['message'])
