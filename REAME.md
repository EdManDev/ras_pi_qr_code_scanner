# Raspberry Pi QR Code Scanner

A Python-based QR code scanner specifically designed for Raspberry Pi 4B with OV5647 camera running Ubuntu 22.04.5 LTS ARM.

## Features

- Real-time QR code scanning using the Raspberry Pi camera
- Multiple display modes (normal, grayscale, threshold)
- Auto-detection and reshaping of camera frames
- Support for saving detected QR codes to a file
- Debug options for troubleshooting

 Point your camera at a QR code
 
 3. The application will:
   - Display the live camera feed
   - Draw green boxes around detected QR codes
   - Show the decoded data on screen
   - Print the decoded data to the console
   Press 'q' to quit the application


## Prerequisites

### Hardware
- Raspberry Pi 4B
- OV5647 camera module properly connected
- Display (if using visualization features)

### Software
- Ubuntu 22.04.5 LTS ARM
- Python 3.8+

## Installation

### 1. Update your system
```bash
sudo apt update
sudo apt upgrade -y
```

### 2. Install essential dependencies
```bash
sudo apt install -y python3-pip python3-dev python3-opencv v4l-utils libopencv-dev
```

### 3. Install Python packages
```bash
pip3 install opencv-python
pip3 install pyzbar
pip3 install numpy
```

### 4. (Optional) Camera setup
Ensure your user has permission to access the camera:
```bash
sudo usermod -a -G video $USER
```
Log out and log back in for the changes to take effect.

## Usage

### Basic Usage
```bash
python3 qr_scanner.py
```

### Show camera feed and scan QR codes
```bash
python3 qr_scanner.py --show
```

### Save detected QR codes to a file
```bash
python3 qr_scanner.py --output detected_codes.txt
```

### Debug camera issues
```bash
python3 qr_scanner.py --debug --show
```

### Save a single frame for troubleshooting
```bash
python3 qr_scanner.py --save-frame camera_frame.jpg
```

### Change display mode
```bash
python3 qr_scanner.py --show --display-mode threshold
```
Available modes: normal, gray, threshold

### Customize camera resolution
```bash
python3 qr_scanner.py --show --width 320 --height 240
```

## Keyboard Controls

When the display window is active:
- Press `q` to quit the application
- Press `m` to cycle through display modes (normal, gray, threshold)

## Troubleshooting

### Camera not detected
- Check your camera connection
- List available video devices: `ls -la /dev/video*`
- Check camera details: `v4l2-ctl --list-devices`
- Check supported formats: `v4l2-ctl -d /dev/video0 --list-formats-ext`

### Permission issues
- Ensure your user is part of the video group: `sudo usermod -a -G video $USER`
- Check file permissions on video devices: `ls -la /dev/video*`

### Image quality issues
- Try different display modes: `--display-mode threshold`
- Try different resolutions: `--width 320 --height 240`
- Save a frame and examine it: `--save-frame debug.jpg`

## File Structure

- `qr_scanner.py` - Main program
- `detected_codes.txt` - Example output file for detected QR codes

## Dependencies

The application relies on the following Python libraries:
- OpenCV (cv2) - For camera interaction and image processing
- pyzbar - For QR code detection and decoding
- numpy - For array manipulation
- argparse - For command-line argument parsing

## License

This project is open source and available under the MIT License.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Acknowledgments

- The OpenCV team for their excellent computer vision library
- The pyzbar developers for QR code detection capabilities
