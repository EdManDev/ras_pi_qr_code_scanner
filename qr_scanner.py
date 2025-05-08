import cv2
import numpy as np
from pyzbar.pyzbar import decode
from picamera2 import Picamera2

# Initialize the Picamera2 object
picam2 = Picamera2()

# Configure the camera resolution (you can keep the default resolution)
picam2.configure(picam2.create_still_configuration())

# Start the camera
picam2.start()

while True:
    # Capture a frame from the camera
    frame = picam2.capture_array()

    # Resize the frame (e.g., to 640x480)
    frame_resized = cv2.resize(frame, (640, 480))

    # Decode QR codes in the captured frame
    decoded_objects = decode(frame_resized)

    for obj in decoded_objects:
        # Draw a rectangle around the QR code
        points = obj.polygon
        if len(points) == 4:
            points = [(int(point[0]), int(point[1])) for point in points]
            cv2.polylines(frame_resized, [np.array(points, dtype=np.int32)], True, (0, 255, 0), 2)
        else:
            # Handle QR codes with different shapes (e.g., circular, etc.)
            cv2.circle(frame_resized, (int(obj.rect[0]), int(obj.rect[1])), 5, (0, 0, 255), -1)

        # Decode the QR code data
        qr_data = obj.data.decode("utf-8")
        print(f"QR Code detected: {qr_data}")

        # Optionally, display the decoded QR code data on the screen
        cv2.putText(frame_resized, qr_data, (int(obj.rect[0]), int(obj.rect[1]) - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

    # Display the resized frame with the QR code drawn on it
    cv2.imshow('QR Code Scanner', frame_resized)

    # Break the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Clean up
picam2.stop()
cv2.destroyAllWindows()
