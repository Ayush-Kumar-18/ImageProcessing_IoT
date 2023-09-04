import simpy
import cv2
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk


class CameraApp:
    captured_image = None

    def __init__(self, root):
        self.root = root
        self.root.title("Camera Module")

        self.cap = cv2.VideoCapture(0)
        self.updating = True

        # label to display the camera feed
        self.label = ttk.Label(self.root)
        self.label.pack(padx=10, pady=10)

        # Capture button
        self.capture_button = ttk.Button(self.root, text="Capture", command=self.capture_image)
        self.capture_button.pack()

        # Reset button (initially disabled)
        self.reset_button = ttk.Button(self.root, text="Reset", command=self.reset, state=tk.DISABLED)
        self.reset_button.pack()

        # Accept Button
        self.accept_button = ttk.Button(self.root, text="Accept", command=self.accept)
        self.accept_button.pack()

        # Start updating the camera feed
        self.update_frame()

    # Function for update
    def update_frame(self):
        _, frame = self.cap.read()
        if frame is not None:
            # Convert the OpenCV frame to a PIL Image
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(frame)
            img = ImageTk.PhotoImage(image=img)
            self.label.config(image=img)
            self.label.image = img
            self.root.after(10, self.update_frame)

    # Function for capture
    def capture_image(self):
        self.updating = False
        _, frame = self.cap.read()
        if frame is not None:
            self.display_captured_image(frame)
            self.capture_button.config(state=tk.DISABLED)
            self.reset_button.config(state=tk.NORMAL)
            self.cap.release()

    # Function for Displaying captured image
    def display_captured_image(self, frame):
        # Convert the OpenCV frame to a PIL Image
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # image
        self.captured_image = frame
        img = Image.fromarray(frame)
        img = ImageTk.PhotoImage(image=img)
        self.label.config(image=img)
        self.label.image = img

    # Function for reset button
    def reset(self):
        self.updating = True
        img = Image.new('RGB', (640, 480))
        img = ImageTk.PhotoImage(image=img)
        self.label.config(image=img)
        self.label.image = img
        self.capture_button.config(state=tk.NORMAL)
        self.reset_button.config(state=tk.DISABLED)
        self.cap.release()
        self.cap.open(0)
        self.update_frame()
        self.captured_image = None

    # Function for accept -- to be updated
    def accept(self):
        pass

    def run(self):
        self.root.mainloop()
        self.cap.release()
        cv2.destroyAllWindows()


class IOT(CameraApp):
    def __init__(self, env, root):
        super().__init__(root)
        self.env = env
        print('Device Is Ready')

    def run(self):
        print('Device Is Running')
        super().run()


env = simpy.Environment()
root = tk.Tk()
camera = IOT(env, root)

# Start the CameraApp run process after creating the IOT instance
camera.run()
