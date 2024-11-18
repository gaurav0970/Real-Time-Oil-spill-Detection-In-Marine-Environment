import cv2
import numpy as np
import tkinter as tk
from tkinter import filedialog, Label, Button, Radiobutton, IntVar
from PIL import Image, ImageTk


# Function to detect oil spill by analyzing dark grey areas in SAR image
def detect_oil_spill(image):
    # Convert the image to grayscale if not already in grayscale
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Apply the black and white (binary threshold) filter for live camera feed
    _, thresholded = cv2.threshold(gray_image, 128, 255, cv2.THRESH_BINARY)

    # Find contours that could represent oil spills
    contours, _ = cv2.findContours(thresholded, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Initialize variables to store oil spill data
    oil_spill_area = 0
    spill_location = (0, 0)
    closed_contours = []

    for contour in contours:
        # Calculate the perimeter of the contour
        perimeter = cv2.arcLength(contour, True)

        # Check if the contour is a closed loop
        if perimeter > 100:  # Arbitrary minimum perimeter length to filter out small contours
            approx = cv2.approxPolyDP(contour, 0.02 * perimeter, True)  # Approximate contour shape
            if len(approx) >= 3:  # We are interested in closed shapes (triangles, polygons, etc.)
                closed_contours.append(contour)

                # Calculate area of the closed contour
                oil_spill_area += cv2.contourArea(contour)

                # Get the center of the contour
                M = cv2.moments(contour)
                if M["m00"] != 0:
                    cX = int(M["m10"] / M["m00"])
                    cY = int(M["m01"] / M["m00"])
                    spill_location = (cX, cY)

    return oil_spill_area, spill_location, closed_contours, thresholded


# Function to update the frame from the camera feed
def update_frame():
    global show_processed_frame
    if camera_mode.get() == 1:  # If camera mode is selected
        ret, frame = cap.read()
        if ret:
            spill_size, location, closed_contours, processed_frame = detect_oil_spill(frame)

            # Invert the colors of the processed frame
            inverted_frame = cv2.bitwise_not(processed_frame)

            # Draw contours on the inverted frame (black and white)
            for contour in closed_contours:
                cv2.drawContours(inverted_frame, [contour], -1, (255, 255, 255), 2)

            # Toggle between the original camera view and processed frame based on the flag
            if show_processed_frame:
                # Convert the processed frame to RGB for displaying in Tkinter
                frame_rgb = cv2.cvtColor(inverted_frame, cv2.COLOR_GRAY2RGB)
            else:
                # Show original frame (color) if not in processed view mode
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            img = Image.fromarray(frame_rgb)
            imgtk = ImageTk.PhotoImage(image=img)
            camera_label.imgtk = imgtk
            camera_label.configure(image=imgtk)

            # Update detection results on the GUI
            if spill_size > 0:
                detection_label.config(text="Detected", fg="green")
                size_label.config(text=f"Size: {spill_size} sq pixels")
                location_label.config(text=f"Location: {location}")
                toggle_button.config(state="normal")  # Enable toggle button if oil is detected
            else:
                detection_label.config(text="Not Detected", fg="red")
                size_label.config(text="Size: N/A")
                location_label.config(text="Location: N/A")
                toggle_button.config(state="disabled")  # Disable toggle button if no oil is detected

    camera_label.after(10, update_frame)  # Refresh the frame every 10 ms


# Toggle between processed and original view
def toggle_view():
    global show_processed_frame
    show_processed_frame = not show_processed_frame


# Function to upload an image using a file dialog
def upload_image():
    global uploaded_image
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.jpeg *.png")])
    if file_path:
        # Read and display the uploaded image
        uploaded_image = cv2.imread(file_path)

        # Perform oil spill detection
        spill_size, location, closed_contours, thresholded = detect_oil_spill(uploaded_image)

        # Resize the image to fit in the window
        resized_image = cv2.resize(uploaded_image, (500, 400))

        # Draw contours on the resized image
        for contour in closed_contours:
            cv2.drawContours(resized_image, [contour], -1, (0, 255, 0), 2)  # Green contours for oil spills

        img_rgb = cv2.cvtColor(resized_image, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(img_rgb)
        imgtk = ImageTk.PhotoImage(image=img)
        camera_label.imgtk = imgtk
        camera_label.configure(image=imgtk)

        # Update detection results on the GUI
        if spill_size > 0:
            detection_label.config(text="Detected", fg="green")
            size_label.config(text=f"Size: {spill_size} sq pixels")
            location_label.config(text=f"Location: {location}")
        else:
            detection_label.config(text="Not Detected", fg="red")
            size_label.config(text="Size: N/A")
            location_label.config(text="Location: N/A")


# Create the main window
window = tk.Tk()
window.title("Oil Spill Detection from SAR Image")
window.geometry("800x600")

# Camera feed label
camera_label = Label(window)
camera_label.pack()

# Radio buttons to switch between camera mode and image upload
camera_mode = IntVar()
camera_mode.set(1)  # Default mode is camera

camera_radio = Radiobutton(window, text="Use Camera", variable=camera_mode, value=1)
camera_radio.pack()

upload_radio = Radiobutton(window, text="Upload Image", variable=camera_mode, value=2)
upload_radio.pack()

# Detection indicator (top right corner)
detection_label = Label(window, text="Not Detected", font=("Arial", 20), fg="red")
detection_label.place(x=650, y=10)

# Spill size, location, and other info display (bottom of the window)
size_label = Label(window, text="Size: N/A", font=("Arial", 15))
size_label.place(x=10, y=500)

location_label = Label(window, text="Location: N/A", font=("Arial", 15))
location_label.place(x=10, y=530)

# Upload button to upload SAR images
upload_button = Button(window, text="Upload SAR Image", command=upload_image, font=("Arial", 15))
upload_button.pack()

# Button to toggle between processed and original views
toggle_button = Button(window, text="Toggle View", command=toggle_view, state="disabled", font=("Arial", 15))
toggle_button.pack()

# Initialize the camera
cap = cv2.VideoCapture(0)  # Use 0 for the built-in camera

# Variable to track whether to show the processed frame or the original frame
show_processed_frame = True

# Start the frame update loop
update_frame()

# Run the application
window.mainloop()

# Release the camera after closing the window
cap.release()
cv2.destroyAllWindows()
