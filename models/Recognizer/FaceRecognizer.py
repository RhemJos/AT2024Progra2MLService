from deepface import DeepFace
from .Recognizer import Recognizer
from .DetectedFrame import DetectedFrame
import os


class FaceRecognizer(Recognizer):
    def __init__(self):
        super().__init__()

    def recognize(self, image_path: str, reference_image_path: str, percentage: float = 80.0,
                  word: str = "face") -> DetectedFrame:

        try:
            # Realizar la comparación de rostros
            result = DeepFace.verify(img1_path=reference_image_path, img2_path=image_path)
            similarity_score = result['distance'] if 'distance' in result else None
            print(similarity_score)
            if similarity_score is None:
                print("Error: No similarity score returned.")
                return None

            # Convertimos la distancia en porcentaje de similitud
            similarity_percentage = (1 - similarity_score) * 100

            # Verificamos si el porcentaje de similitud es mayor o igual al requerido
            if similarity_percentage >= percentage:
                detected_frame = DetectedFrame(
                    path=image_path,
                    algorithm='DeepFace',
                    word=word,
                    percentage=round(similarity_percentage, 2),
                    time="00:00:00"  # Tiempo estático; cambiar según disponibilidad de información
                )
                return detected_frame

            print(
                f"No match found with confidence >= {percentage}%. Similarity was {round(similarity_percentage, 2)}%.")
            return None

        except Exception as e:
            print(f"Error during face recognition: {e}")
            return None
