import cv2
import threading
import time

class WebcamStream:
    def __init__(self, src=0):
        self.capture = cv2.VideoCapture(src)
        if not self.capture.isOpened():
            raise ValueError("Could not open webcam.")
        
        # Optimize camera settings for speed
        self.capture.set(cv2.CAP_PROP_FPS, 30)
        
        self.ret, self.frame = self.capture.read()
        self.stopped = False
        self.lock = threading.Lock()

    def start(self):
        """Starts the thread to read frames from the video stream."""
        t = threading.Thread(target=self.update, args=())
        t.daemon = True
        t.start()
        return self

    def update(self):
        """Keep looping infinitely until the stream is stopped."""
        while True:
            if self.stopped:
                return
            
            ret, frame = self.capture.read()
            if ret:
                with self.lock:
                    self.ret = ret
                    self.frame = frame
            else:
                self.stop()

    def read(self):
        """Return the most recent frame."""
        with self.lock:
            return self.ret, self.frame.copy() if self.frame is not None else None

    def stop(self):
        """Indicate that the thread should be stopped."""
        self.stopped = True
        if self.capture.isOpened():
            self.capture.release()
