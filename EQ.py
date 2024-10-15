import sys
import json
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QGridLayout, QSlider, QLabel, QWidget, QPushButton
from PyQt5.QtCore import Qt, QTimer, QThread, pyqtSignal
import pyqtgraph as pg
import gi
gi.require_version('Gst', '1.0')
from gi.repository import Gst
import numpy as np

# Sample JSON configuration (can be loaded from a file)
equalizer_config_json = '''
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
'''

# Load the JSON configuration
equalizer_config = json.loads(equalizer_config_json)

class FrequencyVisualizer(QWidget):
    def __init__(self):
        super().__init__()
        self.graph = pg.PlotWidget()
        self.graph.setYRange(-60, 0)  # dB range
        self.graph.setXRange(20, 20000, padding=0)  # Frequency range from 20Hz to 20kHz
        self.graph.setLabel('left', 'Amplitude (dB)')
        self.graph.setLabel('bottom', 'Frequency (Hz)')
        
        layout = QVBoxLayout()
        layout.addWidget(self.graph)
        self.setLayout(layout)
    
    def update_visualizer(self, frequency_data):
        # Update visualizer with new data
        self.graph.plot(frequency_data, clear=True)

class AudioProcessingThread(QThread):
    frequency_data_signal = pyqtSignal(list)

    def run(self):
        while True:
            # Simulate real-time audio data processing (replace with real audio analysis)
            frequency_data = np.random.rand(31) * -60  # Random dB values for demo
            self.frequency_data_signal.emit(frequency_data)  # Emit the processed data
            self.msleep(100)  # Sleep for 100ms (10Hz update rate)

class PremiumEqualizerApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Premium 31-Band Equalizer with Visualizer')
        self.setGeometry(100, 100, 1200, 800)

        # Initialize layout and GUI components
        main_layout = QVBoxLayout()
        eq_layout = QGridLayout()

        frequencies = ['20Hz', '25Hz', '32Hz', '40Hz', '50Hz', '63Hz', '80Hz', '100Hz', '125Hz', '160Hz',
                       '200Hz', '250Hz', '315Hz', '400Hz', '500Hz', '630Hz', '800Hz', '1kHz', '1.25kHz', '1.6kHz',
                       '2kHz', '2.5kHz', '3.15kHz', '4kHz', '5kHz', '6.3kHz', '8kHz', '10kHz', '12.5kHz', '16kHz', '20kHz']
        
        self.sliders = []
        for i, freq in enumerate(frequencies):
            slider = QSlider(Qt.Vertical)
            slider.setRange(-1000, 1000)
            slider.setTickInterval(100)
            slider.setValue(0)
            slider.setStyleSheet("QSlider::handle:vertical { background-color: #00ff00; height: 20px; margin: -5px; }")
            label = QLabel(freq)
            label.setAlignment(Qt.AlignCenter)
            label.setStyleSheet("color: #ffffff;")
            eq_layout.addWidget(label, 0, i)
            eq_layout.addWidget(slider, 1, i)
            self.sliders.append(slider)
        
        main_layout.addLayout(eq_layout)

        # Add real-time frequency visualizer
        self.visualizer = FrequencyVisualizer()
        main_layout.addWidget(self.visualizer)

        # Apply button
        apply_button = QPushButton('Apply Settings')
        apply_button.setStyleSheet("background-color: #00ff00; color: #000000;")
        apply_button.clicked.connect(self.apply_settings)
        main_layout.addWidget(apply_button)

        # Set the central widget
        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

        # Initialize GStreamer
        Gst.init(None)
        self.pipeline = Gst.Pipeline()
        self.source = Gst.ElementFactory.make('pulsesrc', 'source')
        self.equalizer = Gst.ElementFactory.make('equalizer-nbands', 'equalizer')
        self.equalizer.set_property('num-bands', 31)
        self.sink = Gst.ElementFactory.make('pulsesink', 'sink')

        self.pipeline.add(self.source)
        self.pipeline.add(self.equalizer)
        self.pipeline.add(self.sink)
        self.source.link(self.equalizer)
        self.equalizer.link(self.sink)

        # Apply initial JSON-based configuration to the equalizer
        self.apply_json_config(equalizer_config)

        self.pipeline.set_state(Gst.State.PLAYING)

        # Start the audio processing thread for real-time frequency updates
        self.audio_thread = AudioProcessingThread()
        self.audio_thread.frequency_data_signal.connect(self.visualizer.update_visualizer)
        self.audio_thread.start()

    def apply_json_config(self, config):
        """ Apply the JSON configuration to the equalizer bands """
        bands = config.get('bands', {})
        for band, settings in bands.items():
            frequency = settings.get('frequency')
            gain = settings.get('gain')
            q_factor = settings.get('q')
            filter_type = settings.get('type')

            # Find the matching band by frequency and apply the gain
            for i, slider in enumerate(self.sliders):
                if abs(frequency - float(self.sliders[i].toolTip())) < 1.0:  # Approximate match
                    self.sliders[i].setValue(gain * 100)  # Adjust gain in dB

                    # Additional equalizer settings like `q_factor`, `type`, etc., can be applied here
                    # if your GStreamer equalizer supports such parameters

    def apply_settings(self):
        # Apply the current slider values to the equalizer bands
        for i, slider in enumerate(self.sliders):
            level = slider.value()
            self.equalizer.set_property(f'band{i}', level / 1000.0)  # Convert to millibels

    def closeEvent(self, event):
        # Ensure the GStreamer pipeline is shut down properly
        self.pipeline.set_state(Gst.State.NULL)
        super().closeEvent(event)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = PremiumEqualizerApp()
    window.show()
    sys.exit(app.exec_())
