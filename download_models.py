import urllib.request
import os

# Model URLs
HAND_LANDMARKER_URL = "https://storage.googleapis.com/mediapipe-models/hand_landmarker/hand_landmarker/float16/1/hand_landmarker.task"
FACE_LANDMARKER_URL = "https://storage.googleapis.com/mediapipe-models/face_landmarker/face_landmarker/float16/1/face_landmarker.task"

def download_model(url, filename):
    """Download a model file if it doesn't exist."""
    if os.path.exists(filename):
        print(f"✓ {filename} already exists")
        return
    
    print(f"Downloading {filename}...")
    try:
        urllib.request.urlretrieve(url, filename)
        print(f"✓ Downloaded {filename}")
    except Exception as e:
        print(f"✗ Failed to download {filename}: {e}")

if __name__ == "__main__":
    print("Downloading MediaPipe model files...")
    download_model(HAND_LANDMARKER_URL, "hand_landmarker.task")
    download_model(FACE_LANDMARKER_URL, "face_landmarker.task")
    print("\nAll models downloaded successfully!")
