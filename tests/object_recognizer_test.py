import unittest
from unittest.mock import Mock, patch

from models.Recognizer.ObjectRecognizer import ObjectRecognizerYolo

class ObjectRecognizerTest(unittest.TestCase):
    def setUp(self):
        self.instance = ObjectRecognizerYolo()
        self.model_path = 'models/Recognizer/yolo11n.pt'

    #Carga de Modelo Exitosa
    def test_load_model_success(self):
        self.instance.model_path = self.model_path
        self.instance.load_model()
        self.assertIsNotNone(self.instance.loaded_model)
        print("El modelo se cargó exitosamente.")

    #Carga de Modelo Fallida
    def test_load_model_failure(self):
        self.instance.model_path = 'yolo12n.pt'
        with self.assertRaises(RuntimeError) as context:
            self.instance.load_model()

        # Verificamos que el mensaje de la excepción contenga "Error al cargar el modelo"
        self.assertIn("Error al cargar el modelo", str(context.exception))

    #Carga de loas labels del modelo
    @patch('builtins.open', new_callable=unittest.mock.mock_open, read_data='{"0": "cat", "1": "dog", "3": "person"}')
    def test_load_labels(self, mock_open):
        # Prueba para verificar la carga de etiquetas desde un archivo JSON
        labels = self.instance.load_labels("fake_labels_path")
        mock_open.assert_called_once_with("fake_labels_path", 'r')
        self.assertEqual(labels, {"0": "cat", "1": "dog", "3": "person"})

    # Verificar que el ID de la palabra es correcto
    def test_word_id_success(self):
        word_id = self.instance.get_word_id("person")
        self.assertEqual(word_id, 0)

    # Verificar que lanza una excepción si la palabra no existe en etiquetas
    def test_word_id_failure(self):
        with self.assertRaises(ValueError) as context:
            self.instance.get_word_id("fish")
        self.assertIn("La palabra clave 'fish' no está en la lista de etiquetas.", str(context.exception))

     # Verificar que lanza una excepción si falta la palabra
    def test_recognize_missing_word(self):
        with self.assertRaises(ValueError) as context:
            self.instance.recognize("test_path", confidence_threshold=0.1)
        self.assertIn("The 'word' parameter is required.", str(context.exception))

    #Verificacion que el modelo reconoce
    def test_recognize(self):
        image_path = 'uploads/Filexample/persona1_01_10_44.jpeg'
        result = self.instance.recognize(image_path, confidence_threshold=0.5, word='person')

        self.assertIsNotNone(result)
        self.assertEqual(result.word, 'person')
        self.assertTrue(result.percentage >= 0.5)
        self.assertEqual(result.path, image_path)
        self.assertEqual(result.algorithm, "Yolo11")
        self.assertEqual(result.time, "01:10:44")