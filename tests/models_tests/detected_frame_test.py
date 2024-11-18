import unittest
from models.Recognizer.DetectedFrame import DetectedFrame

class TestDetectedFrame(unittest.TestCase):
    def setUp(self):
        self.valid_path = "uploads/Filexample/persona1_01_10_44.jpeg"
        self.invalid_path = "models_tests/uploads/Filexample/persona3.jpeg"
        self.algorithm = "yolo"
        self.word = "person"
        self.percentage = 0.8

    # Test if the object is correctly converted to a JSON string
    def test_to_json(self):
        frame = DetectedFrame(self.valid_path, self.algorithm, self.word, self.percentage, "01:10:44")
        json_data = frame.to_json()
        self.assertIn('"path": "uploads/Filexample/persona1_01_10_44.jpeg"', json_data)
        self.assertIn('"algorithm": "yolo"', json_data)
        self.assertIn('"word": "person"', json_data)
        self.assertIn('"percentage": 0.8', json_data)
        self.assertIn('"second": "01:10:44"', json_data)

    # Test if the string representation is formatted correctly
    def test_str_representation(self):
        frame = DetectedFrame(self.valid_path, self.algorithm, self.word, self.percentage, "01:10:44")
        expected_str = ("DetectedFrame(path=uploads/Filexample/persona1_01_10_44.jpeg, algorithm=yolo, "
                        "word=person, percentage=0.8%, second=01:10:44)")
        self.assertEqual(str(frame), expected_str)

    # Test if the time is correctly extracted from a valid path
    def test_get_time_valid_path(self):
        frame = DetectedFrame(self.valid_path, self.algorithm, self.word, self.percentage, self.valid_path)
        self.assertEqual(frame.get_time(), "01:10:44")

    # Test if the method returns an appropriate message for an invalid path
    def test_get_time_invalid_path(self):
        frame = DetectedFrame(self.invalid_path, self.algorithm, self.word, self.percentage, self.invalid_path)
        self.assertEqual(frame.get_time(), "No valid time found in the text.")

