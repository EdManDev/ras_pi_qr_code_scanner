#!/usr/bin/env python3

import cv2
import numpy as np
from pyzbar.pyzbar import decode
import time
import argparse

def process_frame(frame, target_size=(640, 480)):
    """
    Process a frame: resize it and detect QR codes
    Returns: resized frame with QR code annotations
    """
    # Resize the frame
    resized_frame = cv2.resize(frame, target_size)
    
    # Process frame for QR codes
    decoded_objects = decode(resized_frame)
    
    for obj in decoded_objects:
        # Extract QR code data
        qr_data = obj.data.decode("utf-8")
        print(f"QR Code detected: {qr_data}")
        
        # Draw a rectangle around the QR code
        points = obj.polygon
        if len(points) == 4:
            # Standard square/rectangular QR code
            points = [(int(point.x), int(point.y)) for point in points]
            cv2.polylines(resized_frame, [np.array(points, dtype=np.int32)], True, (0, 255, 0), 3)
        else:
            # Handle QR codes with different shapes
            x, y, w, h = obj.rect
            cv2.rectangle(resized_frame, (x, y), (x + w, y + h), (0, 255, 0), 3)
        
        # Display the decoded QR code data on the screen
        cv2.putText(resized_frame, qr_data, (obj.rect.left, obj.rect.top - 10), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
    
    return resized_frame

def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='QR Code Scanner')
    parser.add_argument('--width', type=int, default=640, help='Width of the display window')
    parser.add_argument('--height', type=int, default=480, help='Height of the display window')
    parser.add_argument('--fps', type=int, default=30, help='Target FPS')
    args = parser.parse_args()
    
    target_size = (args.width, args.height)
    
    try:
        # Try to import Picamera2
        from picamera2 import Picamera2
        
        print("Using PiCamera2 with libcamera")
        
        # Initialize the camera with PiCamera2
        picam2 = Picamera2()
        
        # Configure camera - adjust these settings as needed for your OV5647
        config = picam2.create_preview_configuration(
            main={"size": target_size, "format": "RGB888"},
            controls={"FrameDurationLimits": (1000000 // args.fps, 1000000 // args.fps)}
        )
        picam2.configure(config)
        
        # Start the camera
        picam2.start()
        
        print(f"Camera started successfully at {target_size[0]}x{target_size[1]} @ {args.fps}fps. Press 'q' to quit.")
        
        try:
            # Calculate FPS
            frame_count = 0
            start_time = time.time()
            fps = 0
            
            while True:
                # Capture a frame
                frame = picam2.capture_array()
                
                # Convert BGR to RGB if needed (depends on camera output)
                if frame.shape[2] == 3:  # Check if it's a color image
                    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
                
                # Process the frame
                processed_frame = process_frame(frame, target_size)
                
                # Calculate and display FPS
                frame_count += 1
                if frame_count >= 10:
                    end_time = time.time()
                    elapsed_time = end_time - start_time
                    fps = frame_count / elapsed_time
                    frame_count = 0
                    start_time = time.time()
                
                cv2.putText(processed_frame, f"FPS: {fps:.1f}", (10, 30), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                
                # Display the frame
                cv2.imshow("QR Code Scanner", processed_frame)
                
                # Break the loop if 'q' is pressed
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
                    
        except KeyboardInterrupt:
            print("Program interrupted by user")
        finally:
            # Clean up
            picam2.stop()
            cv2.destroyAllWindows()
            print("Camera stopped and resources released")

    except (ImportError, ModuleNotFoundError) as e:
        print(f"Error importing camera module: {e}")
        print("Falling back to OpenCV camera capture...")
        
        # Fallback to OpenCV's camera capture
        cap = cv2.VideoCapture(0)
        
        if not cap.isOpened():
            print("Error: Could not open camera with OpenCV either.")
            exit(1)
        
        # Set camera properties
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, target_size[0])
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, target_size[1])
        cap.set(cv2.CAP_PROP_FPS, args.fps)
        
        print(f"Camera opened with OpenCV at {target_size[0]}x{target_size[1]} @ {args.fps}fps. Press 'q' to quit.")
        
        try:
            # Calculate FPS
            frame_count = 0
            start_time = time.time()
            fps = 0
            
            while True:
                # Capture frame
                ret, frame = cap.read()
                
                if not ret:
                    print("Failed to grab frame")
                    break
                    
                # Process the frame
                processed_frame = process_frame(frame, target_size)
                
                # Calculate and display FPS
                frame_count += 1
                if frame_count >= 10:
                    end_time = time.time()
                    elapsed_time = end_time - start_time
                    fps = frame_count / elapsed_time
                    frame_count = 0
                    start_time = time.time()
                
                cv2.putText(processed_frame, f"FPS: {fps:.1f}", (10, 30), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                
                # Display the frame
                cv2.imshow("QR Code Scanner", processed_frame)
                
                # Break the loop if 'q' is pressed
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
        
        except KeyboardInterrupt:
            print("Program interrupted by user")
        finally:
            # Clean up
            cap.release()
            cv2.destroyAllWindows()
            print("Camera stopped and resources released")

if __name__ == "__main__":
    main()