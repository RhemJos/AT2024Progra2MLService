#
# @video_converter.py Copyright (c) 2021 Jalasoft. # 2643 Av Melchor Perez de Olguin, Colquiri Sud, Cochabamba, Bolivia. # <add direccion de jala la paz>
# All rights reserved. #
# This software is the confidential and proprietary information of
# Jalasoft, ("Confidential Information"). You shall not
# disclose such Confidential Information and shall use it only in
# accordance with the terms of the license agreement you entered into
# with Jalasoft.
#

from deepface import DeepFace

from Recognizer import Recognizer


class GenderRecognizer(Recognizer):
    def __init__(self):
        super().__init__()

    def recognize(self, image_path: str, percentage: float = 0.1, word : str =None):
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

