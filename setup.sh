#!/bin/bash

# Face Recognition System Setup Script
# This script sets up the complete face recognition environment

echo "=========================================="
echo "Face Recognition System Setup"
echo "=========================================="

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_PATH="$SCRIPT_DIR/face_recognition_env"

# Check if Homebrew is installed (macOS)
if [[ "$OSTYPE" == "darwin"* ]]; then
    if ! command -v brew &> /dev/null; then
        echo "Error: Homebrew is not installed. Please install Homebrew first:"
        echo "https://brew.sh"
        exit 1
    fi
    
    # Check if cmake is installed
    if ! command -v cmake &> /dev/null; then
        echo "Installing cmake..."
        brew install cmake
    else
        echo "✓ cmake is already installed"
    fi
    
    # Install python-tk for GUI support
    echo "Installing Python tkinter support..."
    brew install python-tk 2>/dev/null || echo "✓ python-tk already installed"
fi

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed. Please install Python 3.7 or later."
    exit 1
fi

echo "✓ Python 3 found: $(python3 --version)"

# Create virtual environment if it doesn't exist
if [ ! -d "$VENV_PATH" ]; then
    echo "Creating virtual environment..."
    python3 -m venv "$VENV_PATH"
else
    echo "✓ Virtual environment already exists"
fi

# Activate virtual environment
echo "Activating virtual environment..."
source "$VENV_PATH/bin/activate"

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo "Installing dependencies..."
pip install setuptools

# Install main packages
echo "Installing face recognition packages..."
pip install cmake dlib opencv-python numpy pillow face-recognition face-recognition-models

echo ""
echo "=========================================="
echo "Setup Complete!"
echo "=========================================="
echo ""
echo "To run the face recognition system:"
echo "  ./run_face_recognition.sh              # Start GUI"
echo "  ./run_face_recognition.sh gui          # Start GUI"
echo "  ./run_face_recognition.sh cli --help   # Command line help"
echo "  ./run_face_recognition.sh example      # Show examples"
echo ""
echo "Or manually:"
echo "  source face_recognition_env/bin/activate"
echo "  python face_recognition_gui.py"
echo ""
echo "Add face images to the 'known_faces' folder to get started!"
