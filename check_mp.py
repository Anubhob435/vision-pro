import sys
print(f"Python Version: {sys.version}")

try:
    import mediapipe as mp
    print(f"MediaPipe Version: {mp.__version__}")
    print(f"MediaPipe Dir: {dir(mp)}")
    
    try:
        from mediapipe import solutions
        print("Success: from mediapipe import solutions")
    except ImportError as e:
        print(f"Failed: from mediapipe import solutions ({e})")

    try:
        import mediapipe.solutions
        print("Success: import mediapipe.solutions")
    except ImportError as e:
        print(f"Failed: import mediapipe.solutions ({e})")
        
except ImportError as e:
    print(f"Failed to import mediapipe: {e}")
