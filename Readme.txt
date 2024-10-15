Premium 31-Band Equalizer with Real-Time Visualizer
Overview
The Premium 31-Band Equalizer is an advanced audio equalizer designed for Linux systems with PulseAudio and GStreamer. It provides fine-grained control over 31 distinct frequency bands, allowing users to tailor audio output for various use cases such as music production, audio enhancement, or personal listening preferences.

This application also includes a real-time frequency visualizer that gives users instant feedback on the audio changes applied via the equalizer sliders.

Features
1. 31-Band Equalizer
Adjust 31 distinct frequency bands from 20Hz to 20kHz.
Each band can be adjusted between -1000 to 1000 millibels (mB), equivalent to ±12 dB for precise control.
Gain control for each band allows for highly customized audio tuning.
Default frequency ranges:
20Hz, 25Hz, 32Hz, 40Hz, 50Hz, 63Hz, 80Hz, 100Hz, 125Hz, 160Hz
200Hz, 250Hz, 315Hz, 400Hz, 500Hz, 630Hz, 800Hz, 1kHz, 1.25kHz, 1.6kHz
2kHz, 2.5kHz, 3.15kHz, 4kHz, 5kHz, 6.3kHz, 8kHz, 10kHz, 12.5kHz, 16kHz, 20kHz
2. Real-Time Frequency Visualizer
Real-time frequency visualization using PyQtGraph.
Displays frequency response from 20Hz to 20kHz in dB.
Provides instant visual feedback as you adjust the equalizer sliders.
Updates at a 100ms interval to maintain smooth and responsive operation.
3. PulseAudio Integration
The application integrates with PulseAudio, allowing you to adjust the equalizer settings for system-wide audio.
Supports input from any source using the pulsesrc GStreamer element and output through pulsesink.
4. Customizable via JSON Configuration
The equalizer can load custom JSON configurations to apply pre-defined equalizer settings.
JSON configuration supports:
Frequency
Gain (dB)
q (quality factor)
Filter type (e.g., Bell, Low Shelf, etc.)
Example of a JSON configuration:
json
Copy code
{
    "mode": "RLC (BT)",
    "bands": {
        "band8": {
            "frequency": 8000.0,
            "gain": 3.0,
            "q": 1.5,
            "type": "Bell"
        },
        "band9": {
            "frequency": 16000.0,
            "gain": 3.0,
            "q": 1.5,
            "type": "Bell"
        }
    },
    "split-channels": false,
    "plugins_order": ["equalizer"]
}
5. Multi-threaded Real-time Processing
The app utilizes QThread to run the frequency analysis and visualizer in the background without affecting UI responsiveness.
Installation
1. System Requirements
Linux operating system with PulseAudio and GStreamer installed.
Python 3.x.
Required Python libraries:
PyQt5
pyqtgraph
GStreamer with Python bindings (gi).
2. Install Required Dependencies
Install PulseAudio (if not already installed):

bash
Copy code
sudo apt install pulseaudio
Install GStreamer and the required plugins:

bash
Copy code
sudo apt install gstreamer1.0-plugins-base gstreamer1.0-plugins-good gstreamer1.0-plugins-bad gstreamer1.0-plugins-ugly
Install PyQt5 and pyqtgraph:

bash
Copy code
sudo apt install python3-pyqt5
pip install pyqtgraph
Install GStreamer Python bindings:

bash
Copy code
sudo apt install python3-gi
3. Running the Application
Clone or download the repository.
Navigate to the directory:
bash
Copy code
cd premium-equalizer
Run the application:
bash
Copy code
python3 premium_equalizer.py
Usage
Adjusting Equalizer Bands
Each slider corresponds to a frequency band. Adjust the slider to increase or decrease the gain for that band.
Upwards increases the gain (boosts that frequency).
Downwards decreases the gain (attenuates that frequency).
Real-time changes are reflected both in the visualizer and the actual audio output.
Apply Button
Once you've adjusted the sliders, press the Apply Settings button to apply the changes to the equalizer.
Real-Time Visualizer
The visualizer displays the amplitude of the frequency spectrum in real-time.
The x-axis shows frequencies from 20Hz to 20kHz, and the y-axis shows amplitude in decibels (dB).
Loading JSON Configuration
You can load a custom equalizer configuration via a JSON file.
To do this, modify the equalizer_config_json variable within the script to match your desired settings.
Example JSON:

json
Copy code
{
    "mode": "RLC (BT)",
    "bands": {
        "band8": {
            "frequency": 8000.0,
            "gain": 3.0,
            "q": 1.5047602375372453,
            "type": "Bell"
        },
        "band9": {
            "frequency": 16000.0,
            "gain": 3.0,
            "q": 1.504760237537245,
            "type": "Bell"
        }
    },
    "split-channels": false,
    "plugins_order": ["equalizer"]
}
Closing the Application
When you close the application, the GStreamer pipeline will be safely shut down.
Technical Details
GStreamer Pipeline:

The application uses GStreamer elements:
pulsesrc: PulseAudio source for system-wide audio capture.
equalizer-nbands: 31-band equalizer for precise audio manipulation.
pulsesink: PulseAudio sink for outputting modified audio.
PyQt5 GUI:

The GUI is built with PyQt5 for managing the sliders, visualizer, and controls.
The equalizer settings are tied to the visual elements (sliders) and can be applied via the GUI.
Multi-threaded Processing:

The application leverages QThread to run background tasks, such as real-time audio analysis and visualization, without blocking the main UI.
Troubleshooting
Common Issues:
No Audio Output:

Ensure PulseAudio is running (pulseaudio --start).
Make sure the GStreamer pipeline is correctly linked, and the PulseAudio sink is set.
Sliders Not Applying Changes:

Double-check if the Apply Settings button is clicked after making slider adjustments.
Real-Time Visualizer Not Updating:

Ensure pyqtgraph is installed (pip install pyqtgraph).
If the visualizer lags, try adjusting the update interval in the AudioProcessingThread.
