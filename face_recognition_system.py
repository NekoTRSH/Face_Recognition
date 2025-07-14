import cv2
import face_recognition
import numpy as np
import pickle
from pathlib import Path
from typing import List, Dict
import argparse

class FaceRecognitionSystem:
    def __init__(self, known_faces_dir: str = "known_faces"):
        """
        Initialize the Face Recognition System
    
        Args:
            known_faces_dir: Directory containing known face images
        """

        self.known_faces_dir = Path(known_faces_dir)
        self.known_face_encodings = []
        self.known_face_names = []
        self.tolerance = 0.6    # Face recognition tolerance (lower = more strict)

        # Create known_faces directory if it doesn't exists
        self.known_faces_dir.mkdir(exist_ok=True)

        # Load known faces
        # self.load_known_faces()

    def load_known_faces(self):
        """ Load and encode all known faces from the known_faces directory """
        print("Loading new faces...")

        # Check if there are any saved encoding files
        encodings_file = self.known_faces_dir / "face_encodings.pkl"
        if encodings_file.exists():
            try:
                with open(encodings_file, 'rb') as f:
                    data = pickle.load(f)
                    self.known_face_encodings = data['encodings']
                    self.known_face_names = data['names']
                print(f"Loaded {len(set(self.known_face_names))} people from cache")
                return
            except:
                print("Error loading cached encodings, rebuilding...")
        
        # Load faces from images
        supported_formats = ('.jpg', '.png', '.jpeg')
        person_encodings = {}   # Dictionary to store multiple encodings per person

        # Check for person folders
        for item in self.known_faces_dir.iterdir():
            if item.is_dir():
                person_name = item.name
                person_face_encodings = []

                print(f"Loading faces for {person_name}...")

                for image_file in item.iterdir():
                    if image_file.suffix.lower() in supported_formats:
                        try:
                            # Load images
                            image = face_recognition.load_image_file(str(image_file))

                            # Get face encodings
                            face_encodings = face_recognition.face_encodings(image)

                            if face_encodings:
                                # Use first face in image
                                person_face_encodings.append(face_encodings[0])
                                print(f"Loaded {image_file.name}")
                            else:
                                print(f"  No face found in {image_file.name}")
                        except Exception as e:
                            print(f"  Error processing {image_file.name}: {str(e)}")
                
                if person_face_encodings:
                    person_encodings[person_name] = person_face_encodings
        
        # Check for individual files in main directory
        for image_file in self.known_faces_dir.iterdir():
            if image_file.is_file() and image_file.suffix.lower() in supported_formats:
                try:
                    # Load image
                    image = face_recognition.load_image_file(str(image_file))
                    
                    # Get face encodings
                    face_encodings = face_recognition.face_encodings(image)
                    
                    if face_encodings:
                        # Use filename (without extension) as the person's name
                        person_name = image_file.stem
                        
                        if person_name not in person_encodings:
                            person_encodings[person_name] = []
                        
                        person_encodings[person_name].append(face_encodings[0])
                        print(f"Loaded face for: {person_name}")
                    else:
                        print(f"No face found in {image_file.name}")
                        
                except Exception as e:
                    print(f"Error processing {image_file.name}: {str(e)}")
        
        # Process collected encodings
        for person_name, encodings_list in person_encodings.items():
            if len(encodings_list) == 1:
                # Only 1 photo, use as is
                self.known_face_encodings.append(encodings_list[0])
                self.known_face_names.append(person_name)
            else:
                # Multiple photos - create an average encoding and add individual ones
                averaged_encoding = np.mean(encodings_list, axis=0)
                self.known_face_encodings.append(averaged_encoding)
                self.known_face_names.append(person_name)

                # Add individual encodings for better recognition
                for i, encoding in enumerate(encodings_list):
                    self.known_face_encodings.append(encoding)
                    self.known_face_names(person_name)
                
                print(f"Created {len(encodings_list) + 1} encodings for {person_name} (averaged + individual)")

        # Save encodings for faster loading next time
        if self.known_face_encodings:
            self.save_encodings()
        
        unique_people = set(self.known_face_names)
        print(f"Total known people loaded: {len(unique_people)}")
        print(f"Total face encodings: {len(self.known_face_encodings)}")
        
        if unique_people:
            print("Known people:", ", ".join(sorted(unique_people)))


    def save_encodings(self):
        """ Save face encodings to file for faster loading """
        encodings_file = self.known_faces_dir / "face_encodings.pkl"
        data = {
            'encodings': self.known_face_encodings,
            'names': self.known_face_names
        }

        with open(encodings_file, 'wb') as f:
            pickle.dump(data, f)
        print("Face encodings saved to cache")


    def add_known_face(self, image_path: str, name: str) -> bool:
        pass

    def recognise_faces_in_image(self, image_path: str) -> List[Dict]:
        """
        Recognise faces in an image
        
        Args:
            image_path: Path to image file
        
        Returns:
            List of dictionaries containing recognition results
        """

        try:
            # Load image, using face_recognition module
            image = face_recognition.load_image_file(image_path)
        except:
            return False
        pass

def main():
    """
    Main function to run rhe face recognition system
    """
    pass

if __name__ == "__main__":
    main()

# testing