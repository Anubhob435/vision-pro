"""
Finger counter module for detecting and counting raised fingers.
"""

class FingerCounter:
    """Counts the number of raised fingers from hand landmarks."""
    
    # Finger tip landmark indices
    THUMB_TIP = 4
    INDEX_TIP = 8
    MIDDLE_TIP = 12
    RING_TIP = 16
    PINKY_TIP = 20
    
    # Finger PIP (middle joint) landmark indices
    THUMB_IP = 3
    INDEX_PIP = 6
    MIDDLE_PIP = 10
    RING_PIP = 14
    PINKY_PIP = 18
    
    # Wrist landmark
    WRIST = 0
    
    def __init__(self):
        pass
    
    def is_finger_up(self, landmarks, tip_id, pip_id):
        """Check if a finger is raised.
        
        Args:
            landmarks: Hand landmarks
            tip_id: Fingertip landmark ID
            pip_id: Finger PIP (middle joint) landmark ID
            
        Returns:
            bool: True if finger is raised, False otherwise
        """
        # For most fingers, check if tip is above PIP joint
        tip = landmarks.landmark[tip_id]
        pip = landmarks.landmark[pip_id]
        
        # Finger is up if tip y-coordinate is less than pip y-coordinate
        # (y increases downward in image coordinates)
        return tip.y < pip.y
    
    def is_thumb_up(self, landmarks, handedness):
        """Check if thumb is raised (special case).
        
        Args:
            landmarks: Hand landmarks
            handedness: 'Left' or 'Right' hand
            
        Returns:
            bool: True if thumb is raised, False otherwise
        """
        thumb_tip = landmarks.landmark[self.THUMB_TIP]
        thumb_ip = landmarks.landmark[self.THUMB_IP]
        
        # For thumb, check horizontal position relative to IP joint
        # Left hand: thumb up if tip.x < ip.x
        # Right hand: thumb up if tip.x > ip.x
        if handedness == 'Right':
            return thumb_tip.x > thumb_ip.x
        else:  # Left hand
            return thumb_tip.x < thumb_ip.x
    
    def count_fingers(self, hand_landmarks, handedness='Right'):
        """Count the number of raised fingers.
        
        Args:
            hand_landmarks: MediaPipe hand landmarks
            handedness: 'Left' or 'Right' hand
            
        Returns:
            int: Number of raised fingers (0-5)
        """
        fingers_up = 0
        
        # Check thumb (special case)
        if self.is_thumb_up(hand_landmarks, handedness):
            fingers_up += 1
        
        # Check other four fingers
        finger_tips = [self.INDEX_TIP, self.MIDDLE_TIP, self.RING_TIP, self.PINKY_TIP]
        finger_pips = [self.INDEX_PIP, self.MIDDLE_PIP, self.RING_PIP, self.PINKY_PIP]
        
        for tip, pip in zip(finger_tips, finger_pips):
            if self.is_finger_up(hand_landmarks, tip, pip):
                fingers_up += 1
        
        return fingers_up
    
    def count_all_hands(self, multi_hand_landmarks, multi_handedness):
        """Count total fingers from all detected hands.
        
        Args:
            multi_hand_landmarks: List of hand landmarks
            multi_handedness: List of hand classifications
            
        Returns:
            tuple: (total_fingers, list of (hand_index, handedness, finger_count))
        """
        total_fingers = 0
        hand_details = []
        
        for idx, (hand_landmarks, hand_info) in enumerate(zip(multi_hand_landmarks, multi_handedness)):
            # Get handedness (Left or Right)
            handedness = hand_info.classification[0].label
            
            # Count fingers for this hand
            finger_count = self.count_fingers(hand_landmarks, handedness)
            total_fingers += finger_count
            
            hand_details.append({
                'index': idx,
                'handedness': handedness,
                'finger_count': finger_count
            })
        
        return total_fingers, hand_details
