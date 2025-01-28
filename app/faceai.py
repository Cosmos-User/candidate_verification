from ast import List, Not
import tempfile
from deepface import DeepFace
# import deepface.DeepFace
from ultralytics import YOLO
import cv2
from dotenv import load_dotenv
import os

load_dotenv()


class FaceAI:
    def __init__(self) -> None:
        self.model_name = os.getenv('YOLO_MODEL')
        self.model = YOLO(self.model_name)

    def register_face(self,):
        pass

    def face_detection(
                        self, 
                        images: str|list):

        results = self.model.predict(images,conf=0.85)        
        return results
    
    def detect_and_crop_face(self, images: str|list):
        """
        This function uses model represented in env for detect, crop and save faces to the local directory

        Args:
        images: Single Image path or List of Image Paths

        """
        try:
            if isinstance(images, str):
                image = cv2.imread(images)

                if image is None:
                    raise ValueError("Image not found or invalid path!")
                
                detected_face = self.model.predict(image, conf=0.85)  
                
                #making the directory if not found
                custom_dir = os.path.join(os.getcwd(), 'cropped_faces')
                os.makedirs(custom_dir, exist_ok=True)
                
                faces_image_paths = []

                if detected_face:
                    for r in detected_face:
                        for idx, box in enumerate(r.boxes):
                            x1, y1, x2, y2 = map(int, box.xyxy[0])  
                
                            with tempfile.NamedTemporaryFile(dir=custom_dir, delete=False, suffix=".jpg") as temp_file:
                                cv2.imwrite(temp_file.name, image[y1:y2, x1:x2])
                                faces_image_paths.append(temp_file.name)
                                print(f"Face {idx} written to {temp_file.name}")
                
                return faces_image_paths                    
                            
            elif isinstance(images, list):
                faces_image_paths = []
                images = os.listdir(images) #temp variables for testing
                
                for image in images:
                    
                    image = cv2.imread(image)

                    if image is None:
                        raise ValueError("Image not found or invalid path!")
                                          
                    detected_face = self.model.predict(image, conf=0.85)
                    
                    #making the directory if not found
                    custom_dir = os.path.join(os.getcwd(), 'cropped_faces')
                    os.makedirs(custom_dir, exist_ok=True)                    

                    if detected_face:
                        for r in detected_face:
                            for idx, box in enumerate(r.boxes):
                                x1, y1, x2, y2 = map(int, box.xyxy[0])  
                    
                                with tempfile.NamedTemporaryFile(dir=custom_dir, delete=False, suffix=".jpg") as temp_file:
                                    cv2.imwrite(temp_file.name, image[y1:y2, x1:x2])
                                    faces_image_paths.append(temp_file.name)
                                    print(f"Face {idx} written to {temp_file.name}")
                    
                return faces_image_paths                    
                
            else:    
                return {"Cannot Extract face from the image"}
        
        except Exception as e:
            print(e)

    def face_recognition(self,image):
        
        result = DeepFace.find(image,
                               db_path=""
                               )
        pass

    async def detect_emotion(self,image):
        try:
            image = cv2.imread(image)
            if image is None:
                raise ValueError("Image not found or corrupted!")
            
            results = DeepFace.analyze(
                        actions = "emotion",
                        img_path=image,
                detector_backend = "retinaface"
                )
            
            if results:
                emotions = []
                for result in results:
                    dominant_emotion = result.get('dominant_emotion')
                    face_confidence = result.get('face_confidence')
                    emotions.append({
                        "dominant_emotion": dominant_emotion,
                        "face_confidence": face_confidence
                    })
                return {
                    "status": "success",
                    "emotions": emotions
                }
            else:
                return {"status": "failure", "message": "No emotion detected"}

        except Exception as e:
            return {"status": "error", "message": str(e)}

    async def get_face_embeddings(self, media_location):
            try:
                embeddings = []
                file_path = []
                
                for dirpath, dirnames, filenames in os.walk("/home/playground/candidate_verification/images/Humans"):
                    for file in filenames:
                        try:
                            img_path = f"{dirpath}/{file}"
                            print(img_path)
                            result =  DeepFace.represent(img_path = img_path, model_name="Facenet512", detector_backend="mtcnn")            
                            for r in result:
                                if r: 
                                    embeddings.append(r.get("embedding"))
                                    file_path.append(img_path)      
                        
                        except Exception as e:
                            print(e)
                
                return {"file_path":file_path,"embeddings":embeddings}
            
            except Exception as e:
                print(e)
                        

    async def face_verification(self, image_one, image_two):
        try:
            results = DeepFace.verify(
                                    image_one, 
                                    image_two,
                                    model_name="ArcFace",
                                    detector_backend="retinaface",
                                    align=True                        
            
                                 )
            
            if results.get('verified'):
                return {"status": "success", "message": "Faces matched"}
            else:
                return {"status": "failure", "message": "Faces don't match"}
        
        except Exception as e:
            return {"status": "error", "message": str(e)}





if __name__ == "__main__":
