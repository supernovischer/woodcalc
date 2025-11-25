import cv2
import numpy as np

def count_piles(image_file, blur_kernel=9, min_dist=30, param1=100, param2=30, min_radius=10, max_radius=100):
    """
    Detects and counts piles in an image using Hough Circle Transform with tunable parameters.
    """
    file_bytes = np.asarray(bytearray(image_file.read()), dtype=np.uint8)
    image = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
    
    if image is None:
        return 0, None

    output = image.copy()
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    if blur_kernel % 2 == 0: blur_kernel += 1
    gray = cv2.GaussianBlur(gray, (blur_kernel, blur_kernel), 2)
    
    circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1.5, min_dist,
                              param1=param1, param2=param2, 
                              minRadius=min_radius, maxRadius=max_radius)
    
    count = 0
    if circles is not None:
        circles = np.uint16(np.around(circles))
        count = len(circles[0, :])
        for i in circles[0, :]:
            cv2.circle(output, (i[0], i[1]), i[2], (0, 255, 0), 2)
            cv2.circle(output, (i[0], i[1]), 2, (0, 0, 255), 3)
            
    output_rgb = cv2.cvtColor(output, cv2.COLOR_BGR2RGB)
    return count, output_rgb

def count_rectangles(image_file, threshold_block_size=11, min_area=100, max_area=5000, min_aspect_ratio=2.0):
    """
    Detects and counts rectangular shapes (boards/beams).
    """
    file_bytes = np.asarray(bytearray(image_file.read()), dtype=np.uint8)
    image = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
    
    if image is None:
        return 0, None

    output = image.copy()
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Ensure block size is odd
    if threshold_block_size % 2 == 0: threshold_block_size += 1
    
    # Adaptive Thresholding
    thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
                                  cv2.THRESH_BINARY_INV, threshold_block_size, 2)
    
    # Morphological ops to separate/clean
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    # Open removes small noise
    opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=1)
    # Dilate slightly to connect broken edges of the same object
    dilated = cv2.dilate(opening, kernel, iterations=1)
    
    contours, _ = cv2.findContours(dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    count = 0
    for cnt in contours:
        area = cv2.contourArea(cnt)
        
        if area < min_area or area > max_area:
            continue
            
        x, y, w, h = cv2.boundingRect(cnt)
        aspect_ratio = float(w) / h if h > 0 else 0
        
        # Check aspect ratio (boards are usually elongated)
        # We allow both horizontal (> ratio) and vertical (< 1/ratio) orientation
        if aspect_ratio > min_aspect_ratio or aspect_ratio < (1.0 / min_aspect_ratio):
            count += 1
            cv2.rectangle(output, (x, y), (x+w, y+h), (0, 255, 0), 2)
            
    output_rgb = cv2.cvtColor(output, cv2.COLOR_BGR2RGB)
    return count, output_rgb
