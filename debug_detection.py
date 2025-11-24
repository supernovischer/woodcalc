import cv2
import numpy as np

image_path = r"C:/Users/allet/.gemini/antigravity/brain/3596aef9-fa96-4902-bc8e-115540a25899/uploaded_image_1763978971117.jpg"

def test_detection(path):
    image = cv2.imread(path)
    if image is None:
        return

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray_blurred = cv2.GaussianBlur(gray, (9, 9), 2)
    
    configs = [
        {"dp": 1.5, "minDist": 35, "param1": 100, "param2": 55, "minRadius": 15, "maxRadius": 80},
        {"dp": 1.5, "minDist": 35, "param1": 100, "param2": 50, "minRadius": 15, "maxRadius": 80},
        {"dp": 1.5, "minDist": 40, "param1": 100, "param2": 55, "minRadius": 15, "maxRadius": 80},
        {"dp": 1.5, "minDist": 40, "param1": 100, "param2": 50, "minRadius": 15, "maxRadius": 80},
    ]

    for i, cfg in enumerate(configs):
        circles = cv2.HoughCircles(gray_blurred, cv2.HOUGH_GRADIENT, 
                                  dp=cfg["dp"], 
                                  minDist=cfg["minDist"],
                                  param1=cfg["param1"], 
                                  param2=cfg["param2"], 
                                  minRadius=cfg["minRadius"], 
                                  maxRadius=cfg["maxRadius"])
        
        count = len(circles[0, :]) if circles is not None else 0
        print(f"Config {i+1}: {cfg} -> Detected {count} circles")

test_detection(image_path)
