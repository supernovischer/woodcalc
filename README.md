# 🌲 Holzpfahl Zähler (Pile Counter)

A Python application that uses Computer Vision to count wooden piles in images and estimate their total mass and volume. Built with **OpenCV** and **Streamlit**.

## ✨ Features

*   **Automated Counting**: Detects wooden piles in images using the Hough Circle Transform.
*   **Mass Estimation**: Calculates estimated mass based on pile count, dimensions, and wood density.
*   **Tunable Detection**: Advanced settings to adjust detection sensitivity, radius, and blur for different image conditions.
*   **Wood Presets**: Built-in density values for common wood types (Robinie, Kastanie, Spruce, etc.).
*   **User-Friendly UI**: Simple web interface to upload images and view results instantly.

## 🚀 Installation

1.  **Clone the repository**:
    ```bash
    git clone https://github.com/supernovischer/woodcalc.git
    cd woodcalc
    ```

2.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

## 💻 Usage

1.  **Run the application**:
    ```bash
    streamlit run app.py
    ```

2.  **Open your browser**: The app should open automatically at `http://localhost:8501`.

3.  **Upload an image**: Select an image of your wooden piles.

4.  **Configure**:
    *   Select the **Wood Type** (Holzart).
    *   Adjust **Dimensions** (Diameter/Length).
    *   Use **Advanced Settings** in the sidebar if the count is inaccurate.

## 🔧 Technologies

*   **Python 3.x**
*   **OpenCV** (Image Processing)
*   **Streamlit** (Frontend)
*   **NumPy** (Calculations)
*   **Pillow** (Image Handling)

## 📝 License

This project is open source.
