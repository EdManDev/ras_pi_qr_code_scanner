# QR Code Scanner

A versatile QR code scanner application capable of running on both Raspberry Pi (using PiCamera2) and standard systems (using OpenCV's camera interface).

## Features

- Real-time QR code detection and decoding
- Support for different QR code shapes
- On-screen display of decoded QR code content
- Configurable resolution and frame rate
- Real-time FPS counter
- Graceful fallback between camera systems

## Requirements

### Hardware
- Raspberry Pi 4B
- OV5647 camera module properly connected

### Software Dependencies
- Python 3.6 or higher
- OpenCV (`cv2`) - For camera access and image processing
- NumPy - For numerical operations
- pyzbar - For QR code detection and decoding
- PiCamera2 - For the Raspberry Pi OV5647 camera module
- Additional packages:
  - argparse - For command-line argument parsing
  - Pillow (optional) - For additional image processing
  - matplotlib (optional) - For visualization if needed

### System Dependencies
- libzbar0 - QR code detection library
- libzbar-dev - Development files for zbar

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/qr-scanner.git
   cd qr-scanner
   ```

2. Create a `requirements.txt` file with the following content:
   ```
   # Core dependencies
   opencv-python>=4.5.0
   numpy>=1.20.0
   pyzbar>=0.1.8

   # For Raspberry Pi camera support
   picamera2>=0.3.12

   # Optional utilities that may be helpful
   argparse>=1.4.0
   Pillow>=8.0.0  # For additional image processing capabilities
   matplotlib>=3.4.0  # For visualization if needed

   # System dependencies (install via apt):
   # sudo apt-get install -y libzbar0 libzbar-dev
   ```

3. Install the required dependencies:

   ### For Raspberry Pi 4B with OV5647 camera:
   ```bash
   # Install system dependencies
   sudo apt update
   sudo apt install -y python3-pip python3-opencv
   sudo apt install -y libzbar0 libzbar-dev
   pip3 install opencv-python numpy pyzbar argparse
   
   # Install Python packages
   pip3 install -r requirements.txt
   ```

   ### For standard systems with webcam:
   ```bash
   # Install system dependencies (if on Linux)
   sudo apt update
   sudo apt install -y libzbar0 libzbar-dev
   
   # Install core Python packages
   pip3 install opencv-python numpy pyzbar argparse
   ```

## Usage

### Basic Usage
Run the script with default settings (640x480 resolution at 30fps):
```bash
python3 qr_code_scanner.py
```

### Custom Configuration
Adjust the resolution and frame rate:
```bash
python3 qr_code_scanner.py --width 800 --height 600 --fps 15
```

### Controls
- Press 'q' to quit the application

## How It Works

1. The script first attempts to use PiCamera2 for Raspberry Pi systems
2. If PiCamera2 is not available, it falls back to OpenCV's camera interface
3. Frames are captured, resized to the specified dimensions
4. QR codes are detected using the pyzbar library
5. Detected QR codes are outlined with a green rectangle
6. The decoded QR code data is displayed on screen
7. FPS (frames per second) is calculated and displayed

## Troubleshooting

### Common Issues

1. **Camera not found**
   - Ensure your camera is properly connected
   - Check if the camera works with other applications
   - Try specifying a different camera index if using OpenCV: `--camera 1`

2. **ImportError: No module named 'picamera2'**
   - This is normal if you're not using a Raspberry Pi
   - The script will automatically fall back to using OpenCV

3. **ImportError: No module named 'pyzbar'**
   - Install the pyzbar library: `pip3 install pyzbar`

4. **Permission denied accessing camera**
   - Run with sudo: `sudo python3 qr_code_scanner.py`
   - Or add your user to the video group: `sudo usermod -a -G video $USER`

### Performance Optimization

- Reduce resolution for better performance on slower systems
- Lower the FPS target if experiencing lag
- Consider using a Raspberry Pi 4 or newer for better performance

## License

[MIT License](LICENSE)

## Acknowledgments

- OpenCV community
- pyzbar developers
- Raspberry Pi foundation
