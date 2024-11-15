import unittest

from models.Recognizer.GenderRecognizer import GenderRecognizer
from models.Recognizer.DetectedFrame import DetectedFrame


class TestGenderRecognizer(unittest.TestCase):
    def setUp(self):
        # Set up the image paths for testing
        self.image_path_woman = "uploads/Filexample/persona2_02_11_23.jpeg"
        self.image_path_man = "uploads/Filexample/persona4_04_05_06.jpeg"
        self.image_path_invalid = "uploads/Filexample/objeto_02_04_13.jpg"
        self.image_path_multiple_faces = 'path_to_image_with_multiple_faces.jpg'

        # Create an instance of GenderRecognizer
        self.recognizer = GenderRecognizer()

    # Test for invalid 'word' parameter
    def test_recognize_invalid_word(self):
        with self.assertRaises(ValueError):
            self.recognizer.recognize(self.image_path_woman, percentage=0.1, word="car")

    # Test for successful detection of gender 'Woman'
    def test_recognize_woman_success(self):
        result = self.recognizer.recognize(self.image_path_woman, percentage=0.5, word="Woman")
        self.assertIsInstance(result, DetectedFrame)
        self.assertEqual(result.word, "Woman")
        self.assertGreaterEqual(result.percentage, 0.5)

    # Test for successful detection of gender 'Man'
    def test_recognize_man_success(self):
        result = self.recognizer.recognize(self.image_path_man, percentage=0.5, word="Man")
        self.assertIsInstance(result, DetectedFrame)
        self.assertEqual(result.word, "Man")
        self.assertGreaterEqual(result.percentage, 0.5)

    # Test when no match is found for the detected gender
    def test_recognize_no_match(self):
        # Set a high percentage to force no matches
        result = self.recognizer.recognize(self.image_path_woman, percentage=0.99, word="Man")
        self.assertIsNone(result)

    # Test for exception handling during analysis (with invalid image)
    def test_recognize_exception_handling(self):
        result = self.recognizer.recognize(self.image_path_invalid, percentage=0.1, word="Woman")
        self.assertIsNone(result)

    # Test when the detected gender does not match the requested 'word'
    def test_recognize_gender_no_match(self):
        result = self.recognizer.recognize(self.image_path_man, percentage=0.5, word="Woman")
        self.assertIsNone(result)

    # Test to verify that the percentage returned is greater than or equal to the requested percentage
    def test_recognize_percentage_check(self):
        result = self.recognizer.recognize(self.image_path_woman, percentage=0.5, word="Woman")
        self.assertGreaterEqual(result.percentage, 0.5)