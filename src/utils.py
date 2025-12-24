import time
import cv2

class FPSMeter:
    def __init__(self):
        self.prev_time = 0
        self.curr_time = 0
        self.fps = 0

    def update(self):
        self.curr_time = time.time()
        delta = self.curr_time - self.prev_time
        if delta > 0:
            self.fps = 1 / delta
        self.prev_time = self.curr_time
        return int(self.fps)

def draw_text_with_background(img, text, pos, font_scale=0.8, thickness=2, text_color=(255, 255, 255), bg_color=(0, 0, 0), padding=5):
    """Draws text with a background rectangle for better visibility."""
    font = cv2.FONT_HERSHEY_SIMPLEX
    (text_w, text_h), _ = cv2.getTextSize(text, font, font_scale, thickness)
    x, y = pos
    cv2.rectangle(img, (x - padding, y - padding - text_h), (x + text_w + padding, y + padding), bg_color, -1)
    cv2.putText(img, text, (x, y), font, font_scale, text_color, thickness)
