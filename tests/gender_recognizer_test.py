import unittest

from models.Recognizer.GenderRecognizer import GenderRecognizer
from models.Recognizer.DetectedFrame import DetectedFrame

class TestGenderRecognizer(unittest.TestCase):

    def setUp(self):
        self.recognizer = GenderRecognizer()
        # Rutas de imágenes de prueba para mujeres y hombres (asegúrate de tener estas imágenes)
        self.image_path_woman = "../uploads/Filexample/persona2_02_11_23.jpeg"
        self.image_path_man = "../uploads/Filexample/persona4_04_05_06.jpeg"
        self.image_path_invalid = "../uploads/Filexample/objeto_02_04_13.jpg"

    # Prueba para el parámetro inválido en 'word'
    def test_recognize_invalid_word(self):
        with self.assertRaises(ValueError):
            self.recognizer.recognize(self.image_path_woman, percentage=0.1, word="car")

    # Prueba para detección exitosa de género 'Woman'
    def test_recognize_woman_success(self):
        result = self.recognizer.recognize(self.image_path_woman, percentage=0.5, word="Woman")
        self.assertIsInstance(result, DetectedFrame)
        self.assertEqual(result.word, "Woman")
        self.assertGreaterEqual(result.percentage, 0.5)

    # Prueba para detección exitosa de género 'Man'
    def test_recognize_man_success(self):
        result = self.recognizer.recognize(self.image_path_man, percentage=0.5, word="Man")
        self.assertIsInstance(result, DetectedFrame)
        self.assertEqual(result.word, "Man")
        self.assertGreaterEqual(result.percentage, 0.5)

    # Prueba para cuando no hay coincidencias en el género detectado
    def test_recognize_no_match(self):
        # Configurar un alto porcentaje para forzar a que no haya coincidencias
        result = self.recognizer.recognize(self.image_path_woman, percentage=0.99, word="Man")
        self.assertIsNone(result)

    # Prueba para el manejo de excepciones durante el análisis (con imagen inválida)
    def test_recognize_exception_handling(self):
        result = self.recognizer.recognize(self.image_path_invalid, percentage=0.1, word="Woman")
        self.assertIsNone(result)
