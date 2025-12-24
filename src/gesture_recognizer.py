import math
import numpy as np


class GestureRecognizer:
    """Recognizes hand gestures from MediaPipe hand landmarks."""
    
    # Configuration
    ROTATION_THRESHOLD = 5.0  # Minimum rotation angle (degrees) to trigger volume change
    SMOOTHING_FACTOR = 0.15   # Volume change smoothing (0-1) - lower = smoother
    VOLUME_CHANGE_RATE = 2.0  # Volume change per degree of rotation
    
    def __init__(self):
        self.current_volume = 50  # Start at 50%
        self.previous_angle = None  # Track previous palm angle
        self.base_angle = None  # Reference angle when palm is centered
        
    def calculate_distance(self, point1, point2):
        """Calculate Euclidean distance between two landmarks.
        
        Args:
            point1: First landmark with x, y, z coordinates
            point2: Second landmark with x, y, z coordinates
            
        Returns:
            float: Euclidean distance between the two points
        """
        return math.sqrt(
            (point1.x - point2.x) ** 2 +
            (point1.y - point2.y) ** 2 +
            (point1.z - point2.z) ** 2
        )
    
    def calculate_palm_angle(self, hand_landmarks):
        """Calculate the rotation angle of the palm.
        
        Uses the angle between wrist and middle finger MCP to determine palm orientation.
        
        Args:
            hand_landmarks: MediaPipe hand landmarks
            
        Returns:
            float: Palm rotation angle in degrees (-90 to 90)
                  Positive = rotated right, Negative = rotated left
        """
        # Get key landmarks
        wrist = hand_landmarks.landmark[0]  # Wrist
        middle_mcp = hand_landmarks.landmark[9]  # Middle finger base
        
        # Calculate angle using arctangent
        # We use x and y coordinates (ignore z for 2D rotation)
        dx = middle_mcp.x - wrist.x
        dy = middle_mcp.y - wrist.y
        
        # Calculate angle in radians, then convert to degrees
        angle_rad = math.atan2(dx, dy)
        angle_deg = math.degrees(angle_rad)
        
        # Normalize to -90 to 90 range
        # 0 degrees = palm facing forward (vertical)
        # Positive = rotated right (clockwise)
        # Negative = rotated left (counter-clockwise)
        
        return angle_deg
    
    def detect_rotation(self, hand_landmarks):
        """Detect palm rotation and calculate volume change.
        
        Args:
            hand_landmarks: MediaPipe hand landmarks
            
        Returns:
            tuple: (current_angle, angle_delta, rotation_direction)
                  rotation_direction: 'right', 'left', or 'none'
        """
        current_angle = self.calculate_palm_angle(hand_landmarks)
        
        # Initialize base angle on first detection
        if self.base_angle is None:
            self.base_angle = current_angle
            self.previous_angle = current_angle
            return current_angle, 0, 'none'
        
        # Calculate angle change from previous frame
        if self.previous_angle is not None:
            angle_delta = current_angle - self.previous_angle
            
            # Determine rotation direction
            if abs(angle_delta) > self.ROTATION_THRESHOLD:
                if angle_delta > 0:
                    rotation_direction = 'right'
                else:
                    rotation_direction = 'left'
            else:
                rotation_direction = 'none'
        else:
            angle_delta = 0
            rotation_direction = 'none'
        
        self.previous_angle = current_angle
        
        return current_angle, angle_delta, rotation_direction
    
    def update_volume_from_rotation(self, angle_delta):
        """Update volume based on rotation angle change.
        
        Args:
            angle_delta: Change in palm angle (degrees)
            
        Returns:
            int: New volume level (0-100)
        """
        # Calculate volume change
        # Positive angle_delta (right rotation) = increase volume
        # Negative angle_delta (left rotation) = decrease volume
        volume_change = angle_delta * self.VOLUME_CHANGE_RATE
        
        # Apply change with smoothing
        target_volume = self.current_volume + volume_change
        
        # Clamp to valid range
        target_volume = max(0, min(100, target_volume))
        
        # Apply smoothing to avoid jitter
        self.current_volume = (
            self.SMOOTHING_FACTOR * target_volume +
            (1 - self.SMOOTHING_FACTOR) * self.current_volume
        )
        
        return int(self.current_volume)
    
    def get_gesture_info(self, hand_landmarks):
        """Get comprehensive gesture information.
        
        Args:
            hand_landmarks: MediaPipe hand landmarks
            
        Returns:
            dict: Gesture information including:
                - palm_angle: float (current palm rotation angle)
                - rotation_direction: str ('right', 'left', or 'none')
                - volume: int (0-100)
                - wrist_pos: tuple (x, y)
                - middle_mcp_pos: tuple (x, y)
        """
        current_angle, angle_delta, rotation_direction = self.detect_rotation(hand_landmarks)
        
        # Update volume based on rotation
        if rotation_direction != 'none':
            volume = self.update_volume_from_rotation(angle_delta)
        else:
            volume = int(self.current_volume)
        
        # Get landmark positions for visual feedback
        wrist = hand_landmarks.landmark[0]
        middle_mcp = hand_landmarks.landmark[9]
        
        return {
            'palm_angle': current_angle,
            'rotation_direction': rotation_direction,
            'volume': volume,
            'wrist_pos': (wrist.x, wrist.y),
            'middle_mcp_pos': (middle_mcp.x, middle_mcp.y)
        }
    
    def reset(self):
        """Reset the gesture recognizer state."""
        self.previous_angle = None
        self.base_angle = None
