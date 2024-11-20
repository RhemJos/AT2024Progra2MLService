from deepface import DeepFace
from .Recognizer import Recognizer
from .DetectedFrame import DetectedFrame
import logging

class FaceRecognizer(Recognizer):
    def __init__(self):
        super().__init__()

    def recognize(self, image_path: str, reference_image_path: str, percentage: float = 80.0,
                  word: str = "face") -> DetectedFrame:

        try:
            # Verify face similarity
            result = DeepFace.verify(img1_path=reference_image_path, img2_path=image_path)
            similarity_score = result['distance'] if 'distance' in result else None
            if similarity_score is None:
                logging.error("No similarity score returned.")
                return None

            # Convert similarity score to a 1-100 value percentage
            similarity_percentage = (1 - similarity_score) * 100

            # Verify the similarity percentage is the value asked in percentage input
            if similarity_percentage >= percentage:
                detected_frame = DetectedFrame(
                    path=image_path,
                    algorithm='DeepFace',
                    word=word,
                    percentage=round(similarity_percentage, 2),
                    time="00:00:00"
                )
                return detected_frame

            logging.warning("No match found with confidence >= %s % Similarity was : %/s", percentage, round(similarity_percentage, 2))
            return None

        except Exception as e:
            logging.error(e)
            return None
