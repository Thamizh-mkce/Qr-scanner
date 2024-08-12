import cv2
from pyzbar.pyzbar import decode
import numpy as np

def scan_qr_code_from_image(image_path):
   
    # Load the image
    image = cv2.imread(image_path)
    decoded_objects = decode(image)

    for obj in decoded_objects:
        print(f"Type: {obj.type}")
        print(f"Data: {obj.data.decode('utf-8')}")

        # Draw the bounding box
        points = obj.polygon
        if len(points) > 4:
            hull = cv2.convexHull(np.array([point for point in points], dtype=np.float32))
            points = list(map(tuple, np.squeeze(hull)))
        else:
            points = [point for point in points]

        for j in range(len(points)):
            cv2.line(image, points[j], points[(j + 1) % len(points)], (0, 255, 0), 3)

    # Show the image
    cv2.imshow("Image", image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def scan_qr_code_from_camera():
    """
    Scans and decodes a QR code from the webcam feed.
    """
    # Initialize the camera
    cap = cv2.VideoCapture(0)

    print("Scanning QR code... Press 'q' to quit.")

    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()
        if not ret:
            break

        decoded_objects = decode(frame)

        for obj in decoded_objects:
            print(f"Type: {obj.type}")
            print(f"Data: {obj.data.decode('utf-8')}")

            # Draw the bounding box
            points = obj.polygon
            if len(points) > 4:
                hull = cv2.convexHull(np.array([point for point in points], dtype=np.float32))
                points = list(map(tuple, np.squeeze(hull)))
            else:
                points = [point for point in points]

            for j in range(len(points)):
                cv2.line(frame, points[j], points[(j + 1) % len(points)], (0, 255, 0), 3)

        # Display the resulting frame
        cv2.imshow("Camera", frame)

        # Exit when 'q' key is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the camera and close windows
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    # Scan QR code from an image
    image_path = "myqr.png"  # Replace with your image path
    scan_qr_code_from_image(image_path)

    # Scan QR code from camera
    scan_qr_code_from_camera()
