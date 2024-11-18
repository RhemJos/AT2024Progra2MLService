import unittest
import os
import zipfile
from io import BytesIO
from werkzeug.datastructures import FileStorage
from utils.file_utils import allowed_file, save_file, extract_zip, download_file_from_url, save_image


class FileUtilsTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Setting up the test environment (upload folder)
        cls.upload_folder = os.path.abspath(os.path.join(
            os.path.dirname(__file__),'.', 'uploads'))
        if not os.path.exists(cls.upload_folder):
            os.makedirs(cls.upload_folder)

    def tearDown(self):
        # Clean up files after each test
        for filename in os.listdir(self.upload_folder):
            file_path = os.path.join(self.upload_folder, filename)
            if os.path.isfile(file_path):
                os.remove(file_path)

    def test_allowed_file_valid_extension(self):
        # Test if the file extension is valid
        valid_files = ['image.png', 'photo.jpg', 'pic.jpeg', 'icon.gif']
        for file_name in valid_files:
            with self.subTest(file=file_name):
                self.assertTrue(allowed_file(file_name))

    def test_allowed_file_invalid_extension(self):
        # Test if the file extension is invalid
        invalid_files = ['document.pdf', 'audio.mp3', 'video.mp4']
        for file_name in invalid_files:
            with self.subTest(file=file_name):
                self.assertFalse(allowed_file(file_name))

    def test_save_file_valid(self):
        # Test the save file function with a valid file
        file_data = BytesIO(b"fake image content")
        file = FileStorage(stream=file_data, filename='image.png')
        file_path = save_file(file)
        self.assertTrue(file_path.endswith('uploads/image.png'))
        self.assertTrue(os.path.exists(file_path))

    def test_save_file_invalid(self):
        # Test the save file function with an invalid file extension
        file_data = BytesIO(b"fake content")
        file = FileStorage(stream=file_data, filename='invalid.txt')
        file_path = save_file(file)
        self.assertIsNone(file_path)

    def test_extract_zip_valid(self):
        # Test the extract zip function with a valid zip file
        zip_filename = 'test.zip'
        zip_path = os.path.join(self.upload_folder, zip_filename)

        # Create a test zip file
        with zipfile.ZipFile(zip_path, 'w') as zipf:
            zipf.writestr('testfile.txt', 'This is a test file.')

        extract_folder = os.path.join(self.upload_folder, 'extracted')
        extracted_folder = extract_zip(zip_path, extract_folder)

        # Check if the zip file was successfully extracted
        self.assertTrue(os.path.exists(extracted_folder))
        self.assertTrue(os.path.exists(os.path.join(extracted_folder, 'testfile.txt')))

        # Clean up the test zip file
        os.remove(zip_path)

    def test_extract_zip_file_not_found(self):
        # Test the extract zip function with a non-existent zip file
        non_existent_zip_path = os.path.join(self.upload_folder, 'non_existent.zip')
        extract_folder = os.path.join(self.upload_folder, 'extracted')

        # Check if FileNotFoundError is raised
        with self.assertRaises(FileNotFoundError):
            extract_zip(non_existent_zip_path, extract_folder)

    def test_download_file_from_url_valid(self):
        # Test the download file from URL function with a valid URL
        url = 'https://drive.google.com/uc?export=download&id=15m-a4lg37vu5jW83GyUzwRQBFTsSedd7'
        file_path = download_file_from_url(url)
        self.assertTrue(file_path.endswith('.zip'))

    def test_download_file_from_url_invalid(self):
        # Test the download file from URL function with an invalid URL
        invalid_url = 'http://invalid-url.com/fake.zip'

        # Check if ValueError is raised for an invalid URL
        with self.assertRaises(ValueError):
            download_file_from_url(invalid_url)

    def test_save_image(self):
        # Test the save image function
        file_data = BytesIO(b"fake image content")
        file = FileStorage(stream=file_data, filename='reference_image.jpg')
        file_path = save_image(file)

        # Check if the image was saved successfully
        self.assertTrue(file_path.endswith('uploads/imagen de referencia'))
        self.assertTrue(os.path.exists(file_path))

