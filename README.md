# face-recognition-attendance-system

# Simple Attendance System

A simple attendance system built with Python using OpenCV for face detection and Tkinter for the GUI.

## Features
- Take attendance using face detection
- View attendance records for the current day

## Requirements
- Python 3.x
- OpenCV
- NumPy
- Pandas
- Tkinter
- PIL (Pillow)

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/simple-attendance-system.git
   cd simple-attendance-system
   ```

2. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

## Usage
Run the main script to start the application:
```bash
python FRAS/main.py
```

## How It Works
- The application uses OpenCV to detect faces from the webcam.
- When a face is detected, attendance is marked automatically.
- Attendance records are stored in CSV files in the `Attendance` directory.

## License
This project is licensed under the MIT License - see the LICENSE file for details.
