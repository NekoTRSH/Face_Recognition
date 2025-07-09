import cv2
import face_recognition
import numpy as np
import pickle
from pathlib import Path
from typing import List, Dict
import argparse

class FaceRecognitionSystem:
    def __init__(self, known_faces_dir: str = "known_faces"):
        self.known_faces_dir = Path(known_faces_dir)
        self.known_face_encoding = []
        self.known_face_names = []
        self.tolerance = 0.6    # Face recognition tolerance (lower = more strict)

        # Create known_faces directory if it doesn't exists
        self.known_faces_dir.mkdir(exist_ok=True)

        # Load known faces
        # self.load_known_faces()
        pass

    def load_known_faces(self):
        pass

    def save_encodings(self):
        pass

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