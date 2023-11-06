import cv2
import tkinter as tk
from tkinter import ttk, filedialog
from PIL import Image, ImageTk

class CameraApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Real-time Pedestrian Detection")

        self.cap = cv2.VideoCapture(0)
        self.updating = True
        self.detecting = False

        # label to display the camera feed
        self.label = ttk.Label(self.root)
        self.label.pack(padx=10, pady=10)

        # Start Detection button
        self.start_detection_button = ttk.Button(self.root, text="Start Detection", command=self.start_detection)
        self.start_detection_button.pack()

        # End Detection button (initially disabled)
        self.end_detection_button = ttk.Button(self.root, text="End Detection", command=self.end_detection, state=tk.DISABLED)
        self.end_detection_button.pack()

        # Test button
        self.test_button = ttk.Button(self.root, text="Test Image", command=self.test_image)
        self.test_button.pack()

        self.pedestrian_count = 0

        # HOG descriptor for pedestrian detection
        self.hog = cv2.HOGDescriptor()
        self.hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

    # Function to update the camera feed
    def update_frame(self):
        if self.detecting:
            _, frame = self.cap.read()
            if frame is not None:
                pedestrians, output_frame = self.detect_pedestrians(frame)
                self.display_frame(output_frame)
                self.pedestrian_count = len(pedestrians)
                print(f"Number of pedestrians detected: {self.pedestrian_count}")
                self.root.after(10, self.update_frame)

    # Function to detect pedestrians using HOG descriptor
    def detect_pedestrians(self, frame):
        pedestrians, weights = self.hog.detectMultiScale(frame)
        for (x, y, w, h) in pedestrians:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        return pedestrians, frame

    # Function to start real-time detection
    def start_detection(self):
        self.detecting = True
        self.start_detection_button.config(state=tk.DISABLED)
        self.end_detection_button.config(state=tk.NORMAL)
        self.update_frame()

    # Function to end detection
    def end_detection(self):
        self.detecting = False
        self.start_detection_button.config(state=tk.NORMAL)
        self.end_detection_button.config(state=tk.DISABLED)

    # Function to test an image file
    def test_image(self):
        file_path = filedialog.askopenfilename(title="Select an Image")
        if file_path:
            image = cv2.imread(file_path)
            pedestrians, output_frame = self.detect_pedestrians(image)
            print(f"Number of pedestrians detected: {len(pedestrians)}")
            self.display_frame(output_frame)

    # Function to display the frame
    def display_frame(self, frame):
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(frame)
        img = ImageTk.PhotoImage(image=img)
        self.label.config(image=img)
        self.label.image = img

    def run(self):
        self.root.mainloop()
        self.cap.release()
        cv2.destroyAllWindows()

app = CameraApp()
app.run()
