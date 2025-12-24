import cv2
import mediapipe as mp
import numpy as np

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
        
        self.mode = mode

    def set_mode(self, mode):
        self.mode = mode

    def process(self, image):
        """Process the image based on current mode."""
        # Convert the BGR image to RGB
        image.flags.writeable = False
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        
        results = {}

        if self.mode == 'hands':
            results['hands'] = self.hands.process(image_rgb)
        elif self.mode == 'face':
            results['face'] = self.face_mesh.process(image_rgb)
        
        # Draw the annotations on the image
        image.flags.writeable = True
        
        if self.mode == 'hands' and results.get('hands') and results['hands'].multi_hand_landmarks:
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

        return image
