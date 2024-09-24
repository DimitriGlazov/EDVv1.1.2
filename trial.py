""" 
Paperless Document Verification 
by D.Rana
Github Repository : 
Compatible when files are uploaded in google drive and similar applications 
V1.1.3
The code is not for open-source purposes solely
"""

# Importing Modules 
import cv2
import pyzbar.pyzbar as pyzbar
import webbrowser
import pygame
import time

# Initialize pygame mixer
pygame.mixer.init()

# Create a window for the QR code scanner
name = 'QR Code Scanner'
cv2.namedWindow(name)

# Camera capture
cap = cv2.VideoCapture(0)
cap.set(3, 1280)  # Width
cap.set(4, 720)   # Height

browser_opened = False  # Flag to track if the browser has been opened
first_detect_time = None  # Variable to store the first detection time

while cap.isOpened():
    success, image = cap.read()

    if not success:
        print("Skipping empty frame")
        continue  # Continue to the next iteration if the frame is empty

    # Decode the QR code in the image
    decoded_objs = pyzbar.decode(image)

    if decoded_objs:
        if first_detect_time is None:
            # Record the time when the QR code is first detected
            first_detect_time = time.time()
            # Play the initial beep sound when QR code is detected
            pygame.mixer.music.load(r"D:\Python\Main Python Directory\Mega Project Prototype 1\Prototype assets\Samsung Notifications - Beep Once.mp3")
            pygame.mixer.music.play()

        # Check if 3 seconds have passed since the QR code was first detected
        if time.time() - first_detect_time >= 1:
            
            for obj in decoded_objs:
                data = obj.data.decode('utf-8')
                print("QR Code Data:", data)
                x, y, w, h = obj.rect
                cv2.rectangle(image, (x, y), (x + w, y + h), (0, 250, 0), 2)

                if not browser_opened:  # Open browser only if it hasn't been opened yet
                    webbrowser.open(data)
                    browser_opened = True  # Set the flag to True after opening the browser

                    # Play the success sound
                    pygame.mixer.music.load(r"d:\Python\Main Python Directory\Mega Project Prototype 1\Prototype assets\QR Success.mp3")
                    pygame.mixer.music.play()

                    time.sleep(5)  # Wait for 5 seconds before resetting
                    browser_opened = False  # Reset the flag to allow future QR code scans

                # Draw a rectangle around the QR code
                
    else:
        # Reset the detection time if no QR code is detected
        first_detect_time = None

    # Show the camera feed
    cv2.imshow(name, image)

    # Exit the loop if the 'Esc' key is pressed
    key = cv2.waitKey(1) & 0xFF
    if key == 27:  # ESC key
        break

# Release the camera and close the OpenCV window
cap.release()
cv2.destroyAllWindows()
