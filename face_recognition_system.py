# import cv2 # Potentially for video recognition
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
        self.load_known_faces()

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
                    self.known_face_names.append(person_name)
                
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
        """
        Add new new known face 

        Args: 
            image_path: Path to the image file
            name: Name of the person

        Returns:
            bool: True if face was successfully added
        """
        try:
            # Load then encode the face
            image = face_recognition.load_image_file(image_path)
            face_encodings = face_recognition.face_encodings(image)

            if not face_encodings:
                print(f"No face found in {image_path}")
                return False
            
            # Create folder if person doesn't exist (name doesn't match)
            person_folder = self.known_faces_dir / name.replace(" ", "_").lower()
            person_folder.mkdir(exist_ok=True)

            # Copy image to person folder with unique name
            image_path_obj = Path(image_path)
            existing_files = list(person_folder.glob(f"{name.replace(' ', '_').lower()}_*{image_path_obj.suffix}"))
            next_number = len(existing_files) + 1

            new_filename = f"{name.replace(' ', '_').lower()}_{next_number}{image_path_obj.suffix}"
            new_image_path = person_folder / new_filename

            # Copy image file
            import shutil
            shutil.copy2(image_path, new_image_path)

            # Add face encoding to current session
            face_encoding = face_encodings[0]
            self.known_face_encodings.append(face_encoding)
            self.known_face_names.append(name)

            # Clear cache encodings for rebuilding next session
            encodings_file = self.known_faces_dir / "face_encodings.pkl"
            if encodings_file.exists():
                encodings_file.unlink()

            print(f"Successfully added {name} (photo #{next_number}) to the system")
            print(f"Image saved as: {new_image_path}")
            return True

        except Exception as e:
            print(f"Error adding face: {str(e)}")
            return False

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

            # Find face location and encoding
            face_locations = face_recognition.face_locations(image)
            face_encodings = face_recognition.face_encodings(image, face_locations)

            results = []

            for face_encoding, face_location in zip(face_encodings, face_locations):
                # Compare the image with the known faces
                matches = face_recognition.compare_faces(
                    self.known_face_encodings, 
                    face_encoding,
                    tolerance=self.tolerance
                )

                name = "Unknown"
                confidence = 0.0

                if True in matches:
                    # Calculate face distances
                    face_distances = face_recognition.face_distance(
                        self.known_face_encodings,
                        face_encoding
                    )

                    # Best match
                    best_match_index = np.argmin(face_distances)

                    if matches[best_match_index]:
                        name = self.known_face_names[best_match_index]
                        confidence = 1 - face_distances[best_match_index]
                
                results.append({
                    'name': name,
                    'confidence': confidence,
                    'location': face_location
                })
            
            return results

        except Exception as e:
            print(f"Error recognising face from image: {str(e)}")
            return []

def main():
    """ Main function to run the face recognition system"""
    # Add arguments when running
    parser = argparse.ArgumentParser(description='Face recognition system')
    parser.add_argument('--mode', choices=['image', 'add'], required=True, help='Recognition mode') # Only image for now
    parser.add_argument('--input', help='Input file path (for image/video mode)')
    parser.add_argument('--output', help='Output file path (for video mode)')
    parser.add_argument('--name', help='Person name (for add mode)')
    parser.add_argument('--tolerance', type=float, default=0.6, 
                       help='Face recognition tolerance (default: 0.6)')
    
    args = parser.parse_args()

    # Initialise face recognition system
    face_system = FaceRecognitionSystem()
    face_system.tolerance = args.tolerance

    if args.mode == 'image':
        if not args.input:
            print("Error: --input required for image mode")
            return
        
        print(f"Recognising faces in image: {args.input}")
        results = face_system.recognise_faces_in_image(args.input)

        if results:
            print("\nRecognition Results:")
            for i, result in enumerate(results, 1):
                print(f"Face {i}: {result['name']} (Confidence: {result['confidence']:.2f})")
        else:
            print("No faces found in the image")

    elif args.mode == 'add':
        if not args.input or not args.name:
            print("Error: --input and --name required for add mode")
            return
        
        success = face_system.add_known_face(args.input, args.name)
        if success:
            print(f"Successfully added {args.name} to system")
        else:
            print(f"Failed to add {args.name} to system")

if __name__ == "__main__":
    main()

# testing