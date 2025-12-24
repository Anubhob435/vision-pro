import cv2
import mediapipe as mp
import numpy as np
from .gesture_recognizer import GestureRecognizer
from .volume_controller import VolumeController
from .finger_counter import FingerCounter
from .utils import VolumeBarDrawer, draw_rotation_indicator, draw_gesture_status, draw_finger_count

class VisionProcessor:
    def __init__(self, mode='none'):
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_drawing_styles = mp.solutions.drawing_styles
        
        # Initialize MediaPipe Hands
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            model_complexity=0,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )

        # Initialize MediaPipe Face Mesh
        self.mp_face_mesh = mp.solutions.face_mesh
        self.face_mesh = self.mp_face_mesh.FaceMesh(
            max_num_faces=1,
            refine_landmarks=True,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )

        # Initialize MediaPipe Pose
        self.mp_pose = mp.solutions.pose
        self.pose = self.mp_pose.Pose(
            model_complexity=1,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )
        
        # Initialize gesture recognition and volume control
        self.gesture_recognizer = GestureRecognizer()
        self.volume_controller = VolumeController()
        self.volume_bar = VolumeBarDrawer()
        
        # Initialize finger counter
        self.finger_counter = FingerCounter()
        
        self.mode = mode

    def set_mode(self, mode):
        self.mode = mode

    def process(self, image):
        """Process the image based on current mode."""
        # Convert the BGR image to RGB
        image.flags.writeable = False
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        
        results = {}

        if self.mode == 'hands' or self.mode == 'gestures' or self.mode == 'count':
            results['hands'] = self.hands.process(image_rgb)
        elif self.mode == 'face':
            results['face'] = self.face_mesh.process(image_rgb)
        elif self.mode == 'pose':
            results['pose'] = self.pose.process(image_rgb)
        
        # Draw the annotations on the image
        image.flags.writeable = True
        
        # Handle gesture mode
        if self.mode == 'gestures' and results.get('hands') and results['hands'].multi_hand_landmarks:
            # Use the first detected hand for gesture control
            hand_landmarks = results['hands'].multi_hand_landmarks[0]
            
            # Get gesture information
            gesture_info = self.gesture_recognizer.get_gesture_info(hand_landmarks)
            
            # Update system volume
            self.volume_controller.set_volume(gesture_info['volume'])
            
            # Draw hand landmarks
            self.mp_drawing.draw_landmarks(
                image,
                hand_landmarks,
                self.mp_hands.HAND_CONNECTIONS,
                self.mp_drawing_styles.get_default_hand_landmarks_style(),
                self.mp_drawing_styles.get_default_hand_connections_style())
            
            # Draw rotation indicator
            draw_rotation_indicator(
                image,
                gesture_info['wrist_pos'],
                gesture_info['middle_mcp_pos'],
                rotation_direction=gesture_info['rotation_direction']
            )
            
            # Draw volume bar
            self.volume_bar.draw(image, gesture_info['volume'])
            
            # Draw gesture status
            draw_gesture_status(
                image, 
                gesture_info['rotation_direction'],
                gesture_info['palm_angle']
            )
        
        # Handle finger counting mode
        elif self.mode == 'count' and results.get('hands') and results['hands'].multi_hand_landmarks:
            # Count fingers from all hands
            total_fingers, hand_details = self.finger_counter.count_all_hands(
                results['hands'].multi_hand_landmarks,
                results['hands'].multi_handedness
            )
            
            # Draw hand landmarks
            for hand_landmarks in results['hands'].multi_hand_landmarks:
                self.mp_drawing.draw_landmarks(
                    image,
                    hand_landmarks,
                    self.mp_hands.HAND_CONNECTIONS,
                    self.mp_drawing_styles.get_default_hand_landmarks_style(),
                    self.mp_drawing_styles.get_default_hand_connections_style())
            
            # Draw large finger count display
            draw_finger_count(image, total_fingers, hand_details)
        
        # Handle regular hand tracking mode
        elif self.mode == 'hands' and results.get('hands') and results['hands'].multi_hand_landmarks:
            for hand_landmarks in results['hands'].multi_hand_landmarks:
                self.mp_drawing.draw_landmarks(
                    image,
                    hand_landmarks,
                    self.mp_hands.HAND_CONNECTIONS,
                    self.mp_drawing_styles.get_default_hand_landmarks_style(),
                    self.mp_drawing_styles.get_default_hand_connections_style())
                    
        elif self.mode == 'face' and results.get('face') and results['face'].multi_face_landmarks:
            for face_landmarks in results['face'].multi_face_landmarks:
                self.mp_drawing.draw_landmarks(
                    image=image,
                    landmark_list=face_landmarks,
                    connections=self.mp_face_mesh.FACEMESH_TESSELATION,
                    landmark_drawing_spec=None,
                    connection_drawing_spec=self.mp_drawing_styles.get_default_face_mesh_tesselation_style())
                self.mp_drawing.draw_landmarks(
                    image=image,
                    landmark_list=face_landmarks,
                    connections=self.mp_face_mesh.FACEMESH_CONTOURS,
                    landmark_drawing_spec=None,
                    connection_drawing_spec=self.mp_drawing_styles.get_default_face_mesh_contours_style())
        
        elif self.mode == 'pose' and results.get('pose') and results['pose'].pose_landmarks:
            # Draw pose landmarks
            self.mp_drawing.draw_landmarks(
                image,
                results['pose'].pose_landmarks,
                self.mp_pose.POSE_CONNECTIONS,
                landmark_drawing_spec=self.mp_drawing_styles.get_default_pose_landmarks_style())

        return image
