from deepface import DeepFace
import pandas as pd
import os

class FaceRecognizer:
    def face_recognition(self, target_image_path, database_path, model_name='VGG-Face', threshold=0.4):
        if not os.path.isfile(target_image_path):
            print(f"Target image path '{target_image_path}' does not exist or is not a file.")
            return
        if not os.path.isdir(database_path):
            print(f"Database path '{database_path}' does not exist or is not a directory.")
            return

    # Perform face recognition
        result = DeepFace.find(img_path=target_image_path, db_path=database_path, model_name=model_name)

        if result and isinstance(result[0], pd.DataFrame) and not result[0].empty:
            closest_match_distance = result[0].iloc[0]['distance']

            similarity_percentage = (1 - closest_match_distance) * 100

            similarity_percentage = round(similarity_percentage, 2)
            return similarity_percentage

        else:
            print("No matches found")

