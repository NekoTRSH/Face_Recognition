# Face Recognition
A python program that will attempt to identify and/or verify a human face from an image.

## Installation
1. **Clone or download this repositiory**
   ```bash
   git clone https://github.com/NekoTRSH/Face_Recognition.git
   ```
   
2. **Run the setup script**
   ```bash
   ./setup.sh
   ```
   This will automatically :
   - Install cmake (macOS)
   - Install Python tkinter support
   - Create a virtual environment
   - Install all required dependencies
     
3. **Start using the program**
   - Add known faces to system
   ```bash
   python face_recognition_system.py --mode add --input path/to/image.jpg --name "John Doe"
   ```
   - Recognise faces from images
   ```bash
   python face_recognition_system.py --mode image --input path/to/image.jpg

   # With custom tolerance (lower = more strict)
   python face_recognition_system.py --mode image --input path/to/image.jpg --tolerance 0.5
   ```

   
