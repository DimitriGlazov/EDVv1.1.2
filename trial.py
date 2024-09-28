"""
Paperless Document Verification 
by D.Rana
Compatible when files are uploaded in Google Drive and similar applications 
V1.1.3
The code is not for open-source purposes solely
"""

# Importing Modules 
import cv2
import pyzbar.pyzbar as pyzbar
import webbrowser
import pygame
import time
import sys
from PyQt5.QtWidgets import QApplication, QLabel, QVBoxLayout, QWidget
from PyQt5.QtGui import QImage, QPixmap, QIcon
from PyQt5.QtCore import QTimer

# Initialize pygame mixer
pygame.mixer.init()

class QRScannerApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.cap = cv2.VideoCapture(0)
        self.cap.set(3, 1280)  # Width
        self.cap.set(4, 720)   # Height
        self.browser_opened = False
        self.first_detect_time = None
        self.qr_data = None

        # Timer to update the video feed
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(2)

    def initUI(self):
        # Set up the window
        self.setWindowTitle("EDV")
        self.setWindowIcon(QIcon(r"D:\Python\Main Python Directory\Mega Project Prototype 1\Prototype assets\qricon.ico"))
        
        # Set up layout and video display label
        self.image_label = QLabel(self)
        layout = QVBoxLayout()
        layout.addWidget(self.image_label)
        self.setLayout(layout)
        
        self.show()

    def update_frame(self):
        success, image = self.cap.read()
        if not success:
            return

        # Decode the QR code in the image
        decoded_objs = pyzbar.decode(image)
        

        if decoded_objs:
            if self.first_detect_time is None:
                
                # Record the time when the QR code is first detected
                self.first_detect_time = time.time()
                
                # Play the initial beep sound when QR code is detected
                pygame.mixer.music.load(r"D:\Python\Main Python Directory\Mega Project Prototype 1\Prototype assets\Samsung Notifications - Beep Once.mp3")
                pygame.mixer.music.play()

            # Check if 3 seconds have passed since the QR code was first detected
            if time.time() - self.first_detect_time >= 1 and not self.browser_opened:
                for obj in decoded_objs:
                    data = obj.data.decode('utf-8')
                    x, y, w, h = obj.rect
                    cv2.rectangle(image, (x, y), (x + w, y + h), (0, 250, 0), 2)

                    if not self.browser_opened and (self.qr_data is None or self.qr_data != data):
                        # Open the browser with the QR code link
                        webbrowser.open(data)
                        self.browser_opened = True
                        self.qr_data = data

                        # Play the success sound
                        pygame.mixer.music.load(r"d:\Python\Main Python Directory\Mega Project Prototype 1\Prototype assets\QR Success.mp3")
                        pygame.mixer.music.play()

                        # Wait for 5 seconds before allowing the next scan
                        QTimer.singleShot(2000, self.reset_browser_flag)

                    # Draw a rectangle around the QR code
                    
        else:
            # Reset the detection time if no QR code is detected
            self.first_detect_time = None
            self.qr_data = None

        # Convert the image to RGB and display it
        rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        convert_to_qt_format = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(convert_to_qt_format)
        self.image_label.setPixmap(pixmap)

    def reset_browser_flag(self):
        # Reset the flag after 5 seconds to allow future QR code scans
        self.browser_opened = False

    def closeEvent(self, event):
        # Release the camera and close OpenCV window
        self.cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    qr_scanner_app = QRScannerApp()
    sys.exit(app.exec_())
