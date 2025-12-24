"""
Air writing module for drawing on screen using index finger.
"""
import cv2
import numpy as np
from collections import deque


class AirWriter:
    """Allows drawing on screen using index finger as a pen."""
    
    def __init__(self, max_points=512, line_thickness=5):
        """Initialize the air writer.
        
        Args:
            max_points: Maximum number of points to store in drawing buffer
            line_thickness: Thickness of drawn lines
        """
        self.drawing_points = deque(maxlen=max_points)
        self.line_thickness = line_thickness
        self.is_drawing = False
        self.current_color = (0, 255, 0)  # Green by default
        self.canvas = None
        
        # Colors available
        self.colors = {
            'green': (0, 255, 0),
            'blue': (255, 0, 0),
            'red': (0, 0, 255),
            'yellow': (0, 255, 255),
            'white': (255, 255, 255),
            'purple': (255, 0, 255),
            'cyan': (255, 255, 0)
        }
        
    def initialize_canvas(self, shape):
        """Initialize transparent canvas for drawing.
        
        Args:
            shape: Shape of the canvas (height, width, channels)
        """
        if self.canvas is None or self.canvas.shape != shape:
            self.canvas = np.zeros(shape, dtype=np.uint8)
    
    def detect_drawing_gesture(self, hand_landmarks):
        """Detect if user is in drawing mode (index finger extended).
        
        Args:
            hand_landmarks: MediaPipe hand landmarks
            
        Returns:
            tuple: (is_drawing, index_tip_position)
        """
        # Get index finger tip (landmark 8)
        index_tip = hand_landmarks.landmark[8]
        
        # Get index finger PIP (landmark 6)
        index_pip = hand_landmarks.landmark[6]
        
        # Get middle finger tip (landmark 12)
        middle_tip = hand_landmarks.landmark[12]
        
        # Get middle finger PIP (landmark 10)
        middle_pip = hand_landmarks.landmark[10]
        
        # Drawing gesture: index finger up, middle finger down
        index_up = index_tip.y < index_pip.y
        middle_down = middle_tip.y > middle_pip.y
        
        is_drawing = index_up and middle_down
        
        return is_drawing, (index_tip.x, index_tip.y)
    
    def add_point(self, point):
        """Add a point to the drawing buffer.
        
        Args:
            point: Tuple (x, y) in normalized coordinates (0-1)
        """
        self.drawing_points.append(point)
    
    def clear_canvas(self):
        """Clear all drawings."""
        self.drawing_points.clear()
        if self.canvas is not None:
            self.canvas.fill(0)
    
    def change_color(self, color_name):
        """Change drawing color.
        
        Args:
            color_name: Name of color from available colors
        """
        if color_name in self.colors:
            self.current_color = self.colors[color_name]
    
    def draw_on_frame(self, frame):
        """Draw the accumulated points on the frame.
        
        Args:
            frame: Image frame to draw on
        """
        h, w = frame.shape[:2]
        
        # Initialize canvas if needed
        self.initialize_canvas(frame.shape)
        
        # Draw all points on canvas
        if len(self.drawing_points) > 1:
            points_list = list(self.drawing_points)
            for i in range(1, len(points_list)):
                if points_list[i] is None or points_list[i-1] is None:
                    continue
                
                # Convert normalized coordinates to pixel coordinates
                pt1 = (int(points_list[i-1][0] * w), int(points_list[i-1][1] * h))
                pt2 = (int(points_list[i][0] * w), int(points_list[i][1] * h))
                
                # Draw line on canvas
                cv2.line(self.canvas, pt1, pt2, self.current_color, self.line_thickness)
        
        # Overlay canvas on frame
        mask = cv2.cvtColor(self.canvas, cv2.COLOR_BGR2GRAY)
        _, mask = cv2.threshold(mask, 1, 255, cv2.THRESH_BINARY)
        mask_inv = cv2.bitwise_not(mask)
        
        # Black out the drawing area in the frame
        frame_bg = cv2.bitwise_and(frame, frame, mask=mask_inv)
        
        # Take only the drawing from canvas
        canvas_fg = cv2.bitwise_and(self.canvas, self.canvas, mask=mask)
        
        # Combine
        frame[:] = cv2.add(frame_bg, canvas_fg)
    
    def draw_cursor(self, frame, position, is_drawing):
        """Draw cursor at index finger tip.
        
        Args:
            frame: Image frame
            position: Tuple (x, y) in normalized coordinates
            is_drawing: Whether currently drawing
        """
        h, w = frame.shape[:2]
        
        # Convert to pixel coordinates
        px = int(position[0] * w)
        py = int(position[1] * h)
        
        # Draw cursor
        cursor_color = self.current_color if is_drawing else (128, 128, 128)
        cursor_radius = 10 if is_drawing else 8
        
        cv2.circle(frame, (px, py), cursor_radius, cursor_color, -1)
        cv2.circle(frame, (px, py), cursor_radius + 3, (255, 255, 255), 2)
