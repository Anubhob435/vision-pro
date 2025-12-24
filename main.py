import cv2
import sys
from src.camera import WebcamStream
from src.processor import VisionProcessor
from src.utils import FPSMeter, draw_text_with_background

def main():
    print("Initializing Vision Pro...")
    
    try:
        # Initialize components
        # Using src=1 for USB webcam
        try:
            webcam = WebcamStream(src=1).start()
        except ValueError:
            print("USB Webcam (Index 1) not found. Falling back to default (Index 0).")
            webcam = WebcamStream(src=0).start()
            
        processor = VisionProcessor(mode='none')
        fps_meter = FPSMeter()
        
        print("Vision Pro Started.")
        print("Controls:")
        print(" 'f' - Toggle Face Detection")
        print(" 'h' - Toggle Hand Tracking")
        print(" 'p' - Toggle Pose Detection (Body)")
        print(" 'c' - Toggle Finger Counting")
        print(" 'd' - Toggle Air Writing (Draw)")
        print(" 'g' - Toggle Gesture Control (Volume)")
        print(" 'n' - None (Clear)")
        print(" 'q' - Quit")
        print("")
        print("Air Writing Controls:")
        print(" 'x' - Clear canvas")
        print(" 'r' - Red, 'b' - Blue, 'g' - Green")

        while True:
            #Read Frame
            ret, frame = webcam.read()
            
            if not ret or frame is None:
                continue

            # Process Frame
            processed_frame = processor.process(frame)
            
            # FPS Calculation
            fps = fps_meter.update()
            
            # UI Overlay
            mode_text = f"Mode: {processor.mode.upper()}"
            fps_text = f"FPS: {fps}"
            
            draw_text_with_background(processed_frame, mode_text, (20, 40), bg_color=(0, 0, 0))
            draw_text_with_background(processed_frame, fps_text, (20, 80), bg_color=(0, 0, 0))

            # Display
            cv2.imshow("Vision Pro", processed_frame)

            # Input Handling
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                break
            elif key == ord('f'):
                processor.set_mode('face')
            elif key == ord('h'):
                processor.set_mode('hands')
            elif key == ord('p'):
                processor.set_mode('pose')
                print("Pose Detection Mode: Full body tracking")
            elif key == ord('c'):
                processor.set_mode('count')
                print("Finger Counting Mode: Show fingers to camera")
            elif key == ord('d'):
                processor.set_mode('draw')
                print("Air Writing Mode: Point index finger to draw")
            elif key == ord('g'):
                processor.set_mode('gestures')
                print("Gesture Control Mode: Rotate palm to control volume")
            elif key == ord('n'):
                processor.set_mode('none')
            
            # Air writing controls
            elif key == ord('x'):
                if processor.mode == 'draw':
                    processor.air_writer.clear_canvas()
                    print("Canvas cleared")
            elif key == ord('r'):
                if processor.mode == 'draw':
                    processor.air_writer.change_color('red')
                    print("Color: Red")
            elif key == ord('b'):
                if processor.mode == 'draw':
                    processor.air_writer.change_color('blue')
                    print("Color: Blue")

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        if 'webcam' in locals():
            webcam.stop()
        cv2.destroyAllWindows()
        print("Vision Pro Stopped.")

if __name__ == "__main__":
    main()
