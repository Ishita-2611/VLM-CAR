import cv2

def test_camera():
    # Try to open the camera
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print("Error: Could not open camera")
        return
    
    print("Camera opened successfully")
    
    # Try to read a frame
    ret, frame = cap.read()
    if ret:
        print("Successfully captured frame")
        # Save the frame to check if it's working
        cv2.imwrite('test_frame.jpg', frame)
        print("Frame saved as 'test_frame.jpg'")
    else:
        print("Error: Could not capture frame")
    
    # Release the camera
    cap.release()
    print("Camera released")

if __name__ == "__main__":
    test_camera() 