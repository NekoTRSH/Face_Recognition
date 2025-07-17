""" A graphical user interface for the program """

import tkinter as tk
from face_recognition_system import FaceRecognitionSystem

class FaceRecognitionGUI:

    def __init__(self, root):
        self.root = root
        self.root.title("Face Recognition App")
        self.root.geometry("500x500")   # Window size (width x height)

        # Initialise the face recognition system
        self.face_recognition_system = FaceRecognitionSystem()

        self.setup_ui()

    def setup_ui(self):
        pass

    pass

def main ():    
    root = tk.Tk()
    app = FaceRecognitionGUI(root)

    root.mainloop()

if __name__ == "__main__":
    main()