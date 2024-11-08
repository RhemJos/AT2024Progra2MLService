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
from Recognizer import Recognizer
from DetectedFrame import DetectedFrame  # Importamos la clase DetectedFrame

class GenderRecognizer(Recognizer):
    def __init__(self):
        super().__init__()

    def recognize(self, image_path: str, percentage: float = 0.1, word: str = None):
        try:
            analysis = DeepFace.analyze(image_path, actions=['gender'])

            # Verificar si el resultado es una lista y tomar el primer elemento si es el caso
            if isinstance(analysis, list):
                analysis = analysis[0]  # Tomamos el primer rostro detectado

            detected_gender = analysis['gender']
            confidence_score = analysis.get('gender_score', 1.0)  # Si no hay 'gender_score', asumimos 100% de certeza

            # Convertimos el porcentaje de certeza en porcentaje (de 0 a 100)
            similarity_percentage = round(confidence_score * 100, 2)

            # Creamos un objeto DetectedFrame con los valores requeridos
            detected_frame = DetectedFrame(
                path=image_path,
                algorithm='DeepFace',
                word=detected_gender,
                percentage=similarity_percentage,
                time="00:00:00"  # Para este caso usamos el tiempo estático; mas adelante vamos a sacar el dato del nombre de la imagen.
            )

            return detected_frame

        except Exception as e:
            print(f"Error detecting gender: {e}")
            return None
