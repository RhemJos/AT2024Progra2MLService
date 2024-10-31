from deepface import DeepFace

from Recognizer import Recognizer


class GenderRecognizer(Recognizer):
    def __init__(self):
        super().__init__()

    def recognize(self, image_path: str, percentage: float = 0.1, word : str =None, model =None):
        try:
            analysis = DeepFace.analyze(image_path, actions=['gender'])

            # Verificar si el resultado es una lista y tomar el primer elemento si es el caso
            if isinstance(analysis, list):
                analysis = analysis[0]  # Tomamos el primer rostro detectado

            print(f"Detected gender: {analysis['gender']}")
            return analysis['gender']

        except Exception as e:
            print(f"Error detecting gender: {e}")
            return None

