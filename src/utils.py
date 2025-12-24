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


class VolumeBarDrawer:
    """Draws a volume bar with percentage display."""
    
    def __init__(self, position='bottom', height=30, padding=20):
        self.position = position
        self.height = height
        self.padding = padding
    
    def draw(self, img, volume_level):
        """Draw volume bar on image.
        
        Args:
            img: Image to draw on
            volume_level: Volume level (0-100)
        """
        h, w = img.shape[:2]
        
        # Calculate bar dimensions
        bar_width = w - (2 * self.padding)
        bar_height = self.height
        
        if self.position == 'bottom':
            bar_y = h - self.padding - bar_height
        else:  # top
            bar_y = self.padding
        
        bar_x = self.padding
        
        # Draw background (dark gray)
        cv2.rectangle(img, 
                     (bar_x, bar_y), 
                     (bar_x + bar_width, bar_y + bar_height),
                     (40, 40, 40), 
                     -1)
        
        # Draw volume fill (gradient from green to yellow to red)
        fill_width = int((volume_level / 100.0) * bar_width)
        if fill_width > 0:
            # Color based on volume level
            if volume_level < 33:
                color = (0, 255, 0)  # Green
            elif volume_level < 66:
                color = (0, 255, 255)  # Yellow
            else:
                color = (0, 165, 255)  # Orange
            
            cv2.rectangle(img,
                         (bar_x, bar_y),
                         (bar_x + fill_width, bar_y + bar_height),
                         color,
                         -1)
        
        # Draw border
        cv2.rectangle(img,
                     (bar_x, bar_y),
                     (bar_x + bar_width, bar_y + bar_height),
                     (255, 255, 255),
                     2)
        
        # Draw percentage text
        text = f"{volume_level}%"
        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 0.7
        thickness = 2
        (text_w, text_h), _ = cv2.getTextSize(text, font, font_scale, thickness)
        
        text_x = bar_x + (bar_width - text_w) // 2
        text_y = bar_y + (bar_height + text_h) // 2
        
        cv2.putText(img, text, (text_x, text_y), font, font_scale, (255, 255, 255), thickness)

def draw_text_with_background(img, text, pos, font_scale=0.8, thickness=2, text_color=(255, 255, 255), bg_color=(0, 0, 0), padding=5):
    """Draws text with a background rectangle for better visibility."""
    font = cv2.FONT_HERSHEY_SIMPLEX
    (text_w, text_h), _ = cv2.getTextSize(text, font, font_scale, thickness)
    x, y = pos
    cv2.rectangle(img, (x - padding, y - padding - text_h), (x + text_w + padding, y + padding), bg_color, -1)
    cv2.putText(img, text, (x, y), font, font_scale, text_color, thickness)


def draw_rotation_indicator(img, wrist_pos, middle_mcp_pos, rotation_direction='none'):
    """Draw a line showing palm orientation and rotation direction.
    
    Args:
        img: Image to draw on
        wrist_pos: Tuple (x, y) in normalized coordinates (0-1)
        middle_mcp_pos: Tuple (x, y) in normalized coordinates (0-1)
        rotation_direction: 'right', 'left', or 'none'
    """
    h, w = img.shape[:2]
    
    # Convert normalized coordinates to pixel coordinates
    wrist_px = (int(wrist_pos[0] * w), int(wrist_pos[1] * h))
    middle_px = (int(middle_mcp_pos[0] * w), int(middle_mcp_pos[1] * h))
    
    # Choose color based on rotation direction
    if rotation_direction == 'right':
        color = (0, 255, 0)  # Green for right (volume up)
        thickness = 4
    elif rotation_direction == 'left':
        color = (0, 0, 255)  # Red for left (volume down)
        thickness = 4
    else:
        color = (255, 255, 0)  # Cyan for no rotation
        thickness = 3
    
    # Draw line from wrist to middle finger MCP
    cv2.line(img, wrist_px, middle_px, color, thickness)
    
    # Draw circles at key points
    cv2.circle(img, wrist_px, 10, color, -1)  # Wrist
    cv2.circle(img, middle_px, 8, color, -1)  # Middle finger base
    
    # Draw directional arrow
    if rotation_direction == 'right':
        # Draw arrow pointing right
        arrow_start = (middle_px[0] + 20, middle_px[1])
        arrow_end = (middle_px[0] + 60, middle_px[1])
        cv2.arrowedLine(img, arrow_start, arrow_end, (0, 255, 0), 3, tipLength=0.4)
        cv2.putText(img, "VOL UP", (arrow_start[0], arrow_start[1] - 10), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
    elif rotation_direction == 'left':
        # Draw arrow pointing left
        arrow_start = (middle_px[0] - 20, middle_px[1])
        arrow_end = (middle_px[0] - 60, middle_px[1])
        cv2.arrowedLine(img, arrow_start, arrow_end, (0, 0, 255), 3, tipLength=0.4)
        cv2.putText(img, "VOL DOWN", (arrow_end[0] - 20, arrow_start[1] - 10), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)


def draw_gesture_status(img, rotation_direction, palm_angle=0, pos=(20, 120)):
    """Draw gesture control status indicator.
    
    Args:
        img: Image to draw on
        rotation_direction: 'right', 'left', or 'none'
        palm_angle: Current palm rotation angle in degrees
        pos: Position (x, y) for the text
    """
    if rotation_direction == 'right':
        status_text = f"Rotating RIGHT | Angle: {palm_angle:.1f}°"
        color = (0, 255, 0)
    elif rotation_direction == 'left':
        status_text = f"Rotating LEFT | Angle: {palm_angle:.1f}°"
        color = (0, 0, 255)
    else:
        status_text = f"Palm Detected | Angle: {palm_angle:.1f}°"
        color = (255, 255, 0)
    
    draw_text_with_background(img, status_text, pos, bg_color=(0, 0, 0), text_color=color)


def draw_finger_count(img, total_count, hand_details=None):
    """Draw large finger count display.
    
    Args:
        img: Image to draw on
        total_count: Total number of fingers detected
        hand_details: Optional list of hand details
    """
    h, w = img.shape[:2]
    
    # Draw large count in center
    count_text = str(total_count)
    font = cv2.FONT_HERSHEY_DUPLEX  # Use DUPLEX instead of BOLD
    font_scale = 8.0
    thickness = 15
    
    # Get text size
    (text_w, text_h), _ = cv2.getTextSize(count_text, font, font_scale, thickness)
    
    # Center position
    x = (w - text_w) // 2
    y = (h + text_h) // 2
    
    # Draw semi-transparent background
    padding = 40
    overlay = img.copy()
    cv2.rectangle(overlay, 
                 (x - padding, y - text_h - padding),
                 (x + text_w + padding, y + padding),
                 (0, 0, 0),
                 -1)
    cv2.addWeighted(overlay, 0.6, img, 0.4, 0, img)
    
    # Draw count with gradient color based on number
    if total_count == 0:
        color = (128, 128, 128)  # Gray
    elif total_count <= 5:
        color = (0, 255, 0)  # Green
    elif total_count <= 8:
        color = (0, 255, 255)  # Yellow
    else:
        color = (0, 165, 255)  # Orange
    
    cv2.putText(img, count_text, (x, y), font, font_scale, color, thickness)
    
    # Draw label
    label = "FINGERS" if total_count != 1 else "FINGER"
    label_font_scale = 1.2
    label_thickness = 3
    (label_w, label_h), _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, label_font_scale, label_thickness)
    label_x = (w - label_w) // 2
    label_y = y + padding + label_h + 20
    cv2.putText(img, label, (label_x, label_y), cv2.FONT_HERSHEY_SIMPLEX, 
               label_font_scale, (255, 255, 255), label_thickness)
    
    # Draw individual hand counts if available
    if hand_details:
        detail_y = 40
        for hand in hand_details:
            hand_text = f"{hand['handedness']}: {hand['finger_count']}"
            draw_text_with_background(img, hand_text, (20, detail_y), 
                                     font_scale=0.7, text_color=(255, 255, 255))
            detail_y += 35


def draw_air_writing_controls(img):
    """Draw air writing mode controls and instructions.
    
    Args:
        img: Image to draw on
    """
    instructions = [
        "AIR WRITING MODE",
        "Point index finger UP to draw",
        "Fold middle finger DOWN while drawing",
        "Press 'x' to clear canvas",
        "Press 'r' for red, 'b' for blue, 'g' for green"
    ]
    
    y_pos = 30
    for i, text in enumerate(instructions):
        if i == 0:
            # Title
            draw_text_with_background(img, text, (20, y_pos), 
                                     font_scale=1.0, text_color=(0, 255, 255), 
                                     bg_color=(0, 0, 0), thickness=2)
            y_pos += 40
        else:
            # Instructions
            draw_text_with_background(img, text, (20, y_pos), 
                                     font_scale=0.6, text_color=(255, 255, 255), 
                                     bg_color=(0, 0, 0))
            y_pos += 30
