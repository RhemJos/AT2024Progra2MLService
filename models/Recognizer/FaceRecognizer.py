import os
from deepface import DeepFace

def face_recognition(target_image_path, database_path, threshold=0.4):

    if not os.path.isfile(target_image_path):
        print(f"Error: Target image path '{target_image_path}' does not exist or is not a file.")
        return

    if not os.path.isdir(database_path):
        print(f"Error: Database path '{database_path}' does not exist or is not a directory.")
        return

    try:
        result = DeepFace.find(img_path=target_image_path, db_path=database_path, model_name='VGG-Face')
        
        if not result.empty:
            distance = result.iloc[0]['VGG-Face_cosine']
            similarity_percentage = max(0, (1 - (distance / threshold)) * 100)
            print(f"Match found with similarity: {similarity_percentage:.2f}%")
            print(result)
        else:
            print("No match found.")
    
    except Exception as e:
        print(f"An error occurred during face recognition: {e}")