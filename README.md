# Vision Pro 👁️

A real-time computer vision application powered by MediaPipe and OpenCV that provides hand tracking and face mesh detection through your webcam.

![Python](https://img.shields.io/badge/python-3.11+-blue.svg)
![MediaPipe](https://img.shields.io/badge/mediapipe-0.10.14-green.svg)
![OpenCV](https://img.shields.io/badge/opencv-4.11+-red.svg)

## ✨ Features

- **Real-time Hand Tracking**: Detect and track up to 2 hands with 21 landmarks per hand
- **Face Mesh Detection**: High-fidelity 3D face mesh with 468 landmarks
- **Threaded Webcam Stream**: Optimized performance using multi-threading
- **Live FPS Counter**: Monitor application performance in real-time
- **Interactive Controls**: Switch between detection modes on-the-fly
- **Clean UI Overlay**: Mode and FPS display with background for better visibility

## 🎯 Demo

The application provides three modes:
- **Face Detection Mode**: Displays detailed face mesh with tesselation and contours
- **Hand Tracking Mode**: Shows hand landmarks and connections for gesture recognition
- **None Mode**: Clean webcam feed without any overlays

## 🚀 Quick Start

### Prerequisites

- Python 3.11 or higher
- Webcam/Camera device
- [uv](https://github.com/astral-sh/uv) package manager (recommended)

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd vision-pro
   ```

2. **Install dependencies**
   ```bash
   uv sync
   ```

3. **Run the application**
   ```bash
   uv run main.py
   ```

   Or using standard Python:
   ```bash
   python main.py
   ```

## 🎮 Controls

Once the application is running, use these keyboard shortcuts:

| Key | Action |
|-----|--------|
| `f` | Toggle **Face Detection** mode |
| `h` | Toggle **Hand Tracking** mode |
| `n` | Switch to **None** (clear) mode |
| `q` | **Quit** the application |

## 📁 Project Structure

```
vision-pro/
├── main.py                    # Main application entry point
├── src/
│   ├── camera.py             # Threaded webcam stream handler
│   ├── processor.py          # MediaPipe vision processing
│   └── utils.py              # Utility functions (FPS meter, text overlay)
├── pyproject.toml            # Project dependencies
├── download_models.py        # Model download script (for future use)
├── hand_landmarker.task      # MediaPipe hand detection model
├── face_landmarker.task      # MediaPipe face mesh model
└── README.md                 # This file
```

## 🛠️ Technical Details

### Architecture

- **Camera Module** (`camera.py`): Implements threaded video capture for improved performance
- **Processor Module** (`processor.py`): Handles MediaPipe solutions for hand and face detection
- **Utils Module** (`utils.py`): Provides FPS calculation and UI rendering utilities
- **Main Application** (`main.py`): Orchestrates all components and handles user input

### Key Technologies

- **MediaPipe 0.10.14**: Google's cross-platform ML solutions for live perception
- **OpenCV 4.11+**: Computer vision and image processing
- **Threading**: Asynchronous webcam frame capture for better FPS
- **NumPy**: Efficient array operations

### Performance Optimizations

1. **Threaded Webcam Stream**: Separates frame capture from processing
2. **Model Complexity**: Uses lightweight hand detection model (complexity=0)
3. **Optimized Camera Settings**: Set to 30 FPS for balanced performance
4. **Efficient Drawing**: Uses MediaPipe's built-in drawing utilities

## ⚙️ Configuration

You can modify detection parameters in `src/processor.py`:

### Hand Detection
```python
self.hands = self.mp_hands.Hands(
    model_complexity=0,              # 0 (lite) or 1 (full)
    min_detection_confidence=0.5,    # 0.0 to 1.0
    min_tracking_confidence=0.5      # 0.0 to 1.0
)
```

### Face Mesh
```python
self.face_mesh = self.mp_face_mesh.FaceMesh(
    max_num_faces=1,                 # Maximum faces to detect
    refine_landmarks=True,           # Include iris landmarks
    min_detection_confidence=0.5,    # 0.0 to 1.0
    min_tracking_confidence=0.5      # 0.0 to 1.0
)
```

## 🐛 Troubleshooting

### Webcam Not Found
If you see "USB Webcam (Index 1) not found", the application will automatically fall back to the default camera (Index 0). To specify a different camera:

```python
# In main.py, modify the webcam initialization:
webcam = WebcamStream(src=0).start()  # Change 0 to your camera index
```

### MediaPipe Version Issues
This project requires MediaPipe 0.10.14 specifically, as it uses the `solutions` API which was removed in later versions (0.10.15+). If you encounter import errors:

```bash
uv sync  # Reinstall dependencies
```

### Low FPS
- Close other applications using the webcam
- Reduce `max_num_faces` or set `model_complexity=0` for hands
- Lower the camera resolution in `camera.py`

## 📝 Dependencies

Core dependencies (managed via `pyproject.toml`):
- `opencv-python >= 4.11.0.86`
- `mediapipe == 0.10.14`
- `numpy >= 2.4.0`

## 🔮 Future Enhancements

- [ ] Gesture recognition for hand tracking
- [ ] Face emotion detection
- [ ] Recording and playback functionality
- [ ] Multi-camera support
- [ ] Custom landmark visualization styles
- [ ] Export tracking data to JSON/CSV
