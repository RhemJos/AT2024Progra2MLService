"""
 @GenderRecognizer.py Copyright (c) 2021 Jalasoft. # 2643 Av Melchor Perez de Olguin, Colquiri Sud, Cochabamba, Bolivia. # <add direccion de jala la paz>
 All rights reserved. #
 This software is the confidential and proprietary information of
 Jalasoft, ("Confidential Information"). You shall not
 disclose such Confidential Information and shall use it only in
 accordance with the terms of the license agreement you entered into
 with Jalasoft.
"""# pragma: no cover
import logging
from deepface import DeepFace
from .Recognizer import Recognizer
from .DetectedFrame import DetectedFrame  # Importamos la clase DetectedFrame

class GenderRecognizer(Recognizer):
    def __init__(self):
        super().__init__()

    def recognize(self, image_path: str, percentage: float = 0.1, word: str = None):
        if word not in ['Woman', 'Man']:
            logging.error("The 'word' parameter must be either 'Woman' or 'Man'.")
            raise ValueError("The 'word' parameter must be either 'Woman' or 'Man'.")

        try:
            # Analyze the image
            analysis = DeepFace.analyze(image_path, actions=['gender'])

            # If a list get the first element
            if isinstance(analysis, list):
                analysis = analysis[0]  # The first face identified

            detected_gender = analysis['gender']
            woman_percentage = float(detected_gender['Woman'])
            man_percentage = float(detected_gender['Man'])

            # Return the result only the percentage is at least the asked
            if word == 'Woman' and woman_percentage > man_percentage and woman_percentage >= percentage:
                if woman_percentage >= percentage:
                    detected_frame = DetectedFrame(
                        path=image_path,
                        algorithm='DeepFace',
                        word=word,
                        percentage=woman_percentage,
                        time="00:00:00"
                    )
                    return detected_frame
                else:
                    return False
            elif word == 'Man' and man_percentage > woman_percentage and man_percentage >= percentage:
                if man_percentage >= percentage:
                    detected_frame = DetectedFrame(
                        path=image_path,
                        algorithm='DeepFace',
                        word=word,
                        percentage=man_percentage,
                        time="00:00:00"
                    )
                    return detected_frame
                else:
                    return False
            # If there is no face recognized
            logging.info("No matches found for %s  with confidence >= %s", word, percentage)
            return None

        except Exception as e:
            logging.error("Error detecting gender:",e)
            return None