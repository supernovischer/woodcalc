import cv2
import numpy as np

image_path = r"C:/Users/allet/.gemini/antigravity/brain/3596aef9-fa96-4902-bc8e-115540a25899/uploaded_image_1_1764062072237.jpg"

def test_rect_detection_v2(path):
    image = cv2.imread(path)
    if image is None:
        print("Could not read image")
        return

    output = image.copy()
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # 1. Adaptive Thresholding to handle lighting differences
    # Inverts image: Background becomes black, edges/features become white
    thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
                                  cv2.THRESH_BINARY_INV, 11, 2)
    
    # 2. Morphological operations to separate boards
    # Use a horizontal kernel to preserve horizontal structures (gaps)
    # but erode vertically to separate them
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 1))
    eroded = cv2.erode(thresh, kernel, iterations=1)
    dilated = cv2.dilate(eroded, kernel, iterations=1)
    
    # 3. Find Contours
    contours, _ = cv2.findContours(dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    print(f"Total contours found: {len(contours)}")
    
    rect_count = 0
    height, width = image.shape[:2]
    min_area = (width * height) * 0.0005 # 0.05% of image
    max_area = (width * height) * 0.10   # 10% of image
    
    print(f"Filtering area between {min_area:.1f} and {max_area:.1f}")

    for cnt in contours:
        area = cv2.contourArea(cnt)
        
        if area < min_area or area > max_area:
            continue
            
        x, y, w, h = cv2.boundingRect(cnt)
        aspect_ratio = float(w) / h
        
        # Boards are usually much wider than tall in these stacks
        # Filter by aspect ratio (e.g., > 2.0)
        if aspect_ratio > 2.0:
            rect_count += 1
            cv2.rectangle(output, (x, y), (x+w, y+h), (0, 255, 0), 2)
            
    print(f"Filtered Rectangles (Boards): {rect_count}")

test_rect_detection_v2(image_path)
