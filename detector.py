import cv2
import numpy as np

def count_piles(image_file, blur_kernel=9, min_dist=30, param1=100, param2=30, min_radius=10, max_radius=100):
    """
    Detects and counts piles in an image using Hough Circle Transform with tunable parameters.
    """
    # Read image from buffer
    file_bytes = np.asarray(bytearray(image_file.read()), dtype=np.uint8)
    image = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
    
    if image is None:
        return 0, None

    output = image.copy()
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Blur to reduce noise - using GaussianBlur as it handles texture better
    if blur_kernel % 2 == 0: blur_kernel += 1 # Ensure odd
    gray = cv2.GaussianBlur(gray, (blur_kernel, blur_kernel), 2)
    
    # Detect circles
    circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1.5, min_dist,
                              param1=param1, param2=param2, 
                              minRadius=min_radius, maxRadius=max_radius)
    
    count = 0
    if circles is not None:
        circles = np.uint16(np.around(circles))
        count = len(circles[0, :])
        for i in circles[0, :]:
            # draw the outer circle
            cv2.circle(output, (i[0], i[1]), i[2], (0, 255, 0), 2)
            # draw the center of the circle
            cv2.circle(output, (i[0], i[1]), 2, (0, 0, 255), 3)
            
    output_rgb = cv2.cvtColor(output, cv2.COLOR_BGR2RGB)
    
    return count, output_rgb
