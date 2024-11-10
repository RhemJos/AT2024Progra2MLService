#
# @GenderRecognizer.py Copyright (c) 2021 Jalasoft. # 2643 Av Melchor Perez de Olguin, Colquiri Sud, Cochabamba, Bolivia. # <add direccion de jala la paz>
# All rights reserved. #
# This software is the confidential and proprietary information of
# Jalasoft, ("Confidential Information"). You shall not
# disclose such Confidential Information and shall use it only in
# accordance with the terms of the license agreement you entered into
# with Jalasoft.
#
from deepface import DeepFace
from .Recognizer import Recognizer
from .DetectedFrame import DetectedFrame  # Importamos la clase DetectedFrame

class GenderRecognizer(Recognizer):
    def __init__(self):
        super().__init__()

    def recognize(self, image_path: str, percentage: float = 0.1, word: str = None):
        if word not in ['Woman', 'Man']:
            raise ValueError("The 'word' parameter must be either 'Woman' or 'Man'.")

        try:
            # Analizamos la imagen para detectar el género
            analysis = DeepFace.analyze(image_path, actions=['gender'])

            # Verificamos si el resultado es una lista y tomamos el primer elemento si es el caso
            if isinstance(analysis, list):
                analysis = analysis[0]  # Tomamos el primer rostro detectado

            detected_gender = analysis['gender']
            print(detected_gender)
            woman_percentage = detected_gender['Woman']
            man_percentage = detected_gender['Man']

            # Solo devolveremos el resultado si cumple con los criterios de género y porcentaje
            if word == 'Woman' and woman_percentage > man_percentage and woman_percentage >= percentage:
                if woman_percentage >= percentage:
                    detected_frame = DetectedFrame(
                        path=image_path,
                        algorithm='DeepFace',
                        word=word,
                        percentage=woman_percentage,
                        time="00:00:00"  # Tiempo estático para este ejemplo; puede adaptarse si se tiene esta información.
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
            # Si no se cumplen los criterios, devolvemos None indicando que no se encontró coincidencia
            print(f"No matches found for '{word}' with confidence >= {percentage}%.")
            return None

        except Exception as e:
            print(f"Error detecting gender: {e}")
            return None