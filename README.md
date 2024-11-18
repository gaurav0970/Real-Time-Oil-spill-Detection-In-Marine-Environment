**Topic - Real-Time Oil Spill Detection Using SAR Images**

This project implements a real-time oil spill detection system using Synthetic Aperture Radar (SAR) images. The system leverages computer vision techniques to detect dark grey regions in SAR images that may indicate the presence of oil spills in marine environments. The detection process is visualized in real-time through a GUI built with Tkinter, where users can either stream video from a camera or upload SAR images for analysis.

Features:
Real-time oil spill detection: Uses SAR images or live camera feed to detect potential oil spills based on changes in pixel intensities.

1. Image processing: Detects dark grey regions in SAR images using contour-based techniques.

2. User interface: Tkinter-based GUI to display the camera feed or uploaded SAR images with real-time results.

3. Toggle view: Switch between the original image and processed (binary) image that highlights detected oil spills.

4. Location & size information: Displays the size and location of detected oil spills in the image.

**Installation**
To run this project, you'll need Python 3.x and the following Python libraries:

opencv-python (for image and video processing)
numpy (for numerical operations)
tkinter (for the GUI)
Pillow (for image processing and Tkinter compatibility)

You can install the required libraries using pip:

    pip install opencv-python numpy pillow
  
Clone this repository to your local machine:

    git clone https://github.com/your-username/oil-spill-detection.git
    cd oil-spill-detection

      
Running the application
To start the application, simply run the main Python script:

    python oil_spill_detection.py

GUI Features

  1. Camera Mode: Use the built-in webcam to process video frames in real-time. The oil spill detection results will be displayed on the camera feed.
  
  2. Upload Image: Choose an existing SAR image to analyze for potential oil spills.
  
  3. Toggle View: Switch between the original image or live feed and a processed (binary) view showing the detected oil spill regions.
  
  4. Detection Information: Displays the detection status, the size of the detected oil spill, and its location on the image.


**Camera Mode**

In Camera Mode, the system continuously processes the webcam feed, applying the oil spill detection algorithm to detect dark grey regions, which are then highlighted. The system will provide real-time updates on the detected oil spill's size and location.


**Image Upload Mode**

If you have an existing SAR image, you can upload it for processing. After uploading, the system will perform the same oil spill detection process, showing the size and location of any detected oil spills.


**Main Functionality**

The core functionality of this system lies in the detect_oil_spill() function, which performs the following tasks:

1. Converts the image to grayscale.

2. Applies a binary threshold to highlight dark regions (likely oil spills).

3. Detects contours in the thresholded image.

4. Filters contours based on perimeter size and approximates the contour shape.

5. Calculates the area of detected oil spills and determines their locations.

6. The results are displayed in real-time on the GUI.



The Tkinter-based GUI includes:

1. A label for displaying the camera feed or uploaded image.

2. Radio buttons for switching between camera and image upload modes.

3. A toggle button for switching between the processed view and the original view.

4. Labels displaying detection status, size, and location of the oil spill.


**Contributions**
Feel free to fork this repository, open issues, or submit pull requests for any improvements or fixes. Contributions are always welcome!
