import unittest
from models.Recognizer.FaceRecognizer import FaceRecognizer
from models.Recognizer.DetectedFrame import DetectedFrame

class TestFaceRecognizer(unittest.TestCase):

    def setUp(self):
        """
        Set up the FaceRecognizer instance and file paths for testing.
        Ensure these paths point to actual test images in your environment.
        """
        self.recognizer = FaceRecognizer()
        self.valid_image_path = "uploads/Filexample/HK_01_01_01.jpeg"
        self.reference_image_path = "uploads/Filexample/HK_02_02_02.jpg"
        self.non_matching_image_path = "uploads/Filexample/CR_01_01_01.jpg"
        self.invalid_image_path = "models_tests/uploads/Filexample/invalid_01_01_02.jpg"

    #Test successful face recognition when the similarity percentage is met.
    def test_recognize_success(self):
        result = self.recognizer.recognize(
            image_path=self.valid_image_path,
            reference_image_path=self.reference_image_path,
            percentage=0.7
        )
        self.assertIsInstance(result, DetectedFrame)
        self.assertGreaterEqual(result.percentage, 0.7)

    #Test face recognition when no match is found (low similarity).
    def test_recognize_no_match(self):
        result = self.recognizer.recognize(
            image_path=self.non_matching_image_path,
            reference_image_path=self.reference_image_path,
            percentage=90.0
        )
        self.assertIsNone(result)

    #Test face recognition with an invalid image path.
    def test_recognize_invalid_image(self):
        result = self.recognizer.recognize(
            image_path=self.invalid_image_path,
            reference_image_path=self.reference_image_path,
            percentage=70.0
        )
        self.assertIsNone(result)

    #Test face recognition with an invalid reference image path.
    def test_recognize_invalid_reference_image(self):
        result = self.recognizer.recognize(
            image_path=self.valid_image_path,
            reference_image_path=self.invalid_image_path,
            percentage=70.0
        )
        self.assertIsNone(result)

    #Test face recognition with a high similarity percentage threshold.
    def test_recognize_high_percentage_threshold(self):
        result = self.recognizer.recognize(
            image_path=self.valid_image_path,
            reference_image_path=self.reference_image_path,
            percentage=99.9
        )
        self.assertIsNone(result)