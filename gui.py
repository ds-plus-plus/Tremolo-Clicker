import json
import os
from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QSlider, QLabel, QCheckBox, QGroupBox)
from PyQt6.QtCore import Qt, QTimer

class ModernUI(QMainWindow):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller

        self.init_ui()
        self.load_settings()

        self.sync_timer = QTimer(self)
        self.sync_timer.timeout.connect(self.sync_ui_with_controller)
        self.sync_timer.start(100)

    def init_ui(self):
        self.setWindowTitle("Autoclicker")
        self.setFixedSize(450, 320)

        self.setStyleSheet("""
            QMainWindow { background-color: #f8f9fa; }
            QGroupBox { font-weight: bold; margin-top: 15px; border: 1px solid #dee2e6; border-radius: 5px; color: #212529; }
            QGroupBox::title { subcontrol-origin: margin; left: 10px; padding: 0 3px; color: #495057; }
            QLabel { font-size: 12px; color: #212529; }
            QCheckBox { font-size: 12px; color: #212529; }
        """)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(15)

        speed_group = QGroupBox("Timing Parameters")
        speed_layout = QVBoxLayout()

        self.min_lbl = QLabel("Minimum CPS: 5")
        self.min_slider = QSlider(Qt.Orientation.Horizontal)
        self.min_slider.setRange(1, 20)
        self.min_slider.setValue(5)
        self.min_slider.valueChanged.connect(self.update_parameters)

        self.max_lbl = QLabel("Maximum CPS: 13")
        self.max_slider = QSlider(Qt.Orientation.Horizontal)
        self.max_slider.setRange(1, 20)
        self.max_slider.setValue(13)
        self.max_slider.valueChanged.connect(self.update_parameters)

        self.pauses_cb = QCheckBox("Simulate Random Pauses")
        self.pauses_cb.setChecked(False)
        self.pauses_cb.stateChanged.connect(self.update_parameters)

        self.pauses_lbl = QLabel("Pause Frequency: 1")
        self.pauses_slider = QSlider(Qt.Orientation.Horizontal)
        self.pauses_slider.setRange(1, 5)
        self.pauses_slider.setValue(1)
        self.pauses_slider.setEnabled(False)
        self.pauses_lbl.setEnabled(False)
        self.pauses_slider.valueChanged.connect(self.update_parameters)

        speed_layout.addWidget(self.min_lbl)
        speed_layout.addWidget(self.min_slider)
        speed_layout.addWidget(self.max_lbl)
        speed_layout.addWidget(self.max_slider)
        speed_layout.addWidget(self.pauses_cb)
        speed_layout.addWidget(self.pauses_lbl)
        speed_layout.addWidget(self.pauses_slider)
        speed_group.setLayout(speed_layout)

        feature_layout = QHBoxLayout()
        self.clicker_cb = QCheckBox("Enable Autoclicker (DEL)")
        self.clicker_cb.stateChanged.connect(self.toggle_clicker)
        feature_layout.addWidget(self.clicker_cb)

        telemetry_layout = QHBoxLayout()
        self.status_lbl = QLabel("Status: Idle")
        self.clicks_lbl = QLabel("Session Clicks: 0")
        self.clicks_lbl.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        telemetry_layout.addWidget(self.status_lbl)
        telemetry_layout.addWidget(self.clicks_lbl)

        main_layout.addWidget(speed_group)
        main_layout.addLayout(feature_layout)
        main_layout.addLayout(telemetry_layout)

    def load_settings(self):
        if os.path.exists("config.json"):
            try:
                with open("config.json", "r") as f:
                    data = json.load(f)
                    self.min_slider.setValue(data.get("min_cps", 5))
                    self.max_slider.setValue(data.get("max_cps", 13))
                    self.pauses_cb.setChecked(data.get("pauses_enabled", False))
                    self.pauses_slider.setValue(data.get("pause_intensity", 1))
            except:
                pass
        self.update_parameters()

    def closeEvent(self, event):
        data = {
            "min_cps": self.min_slider.value(),
            "max_cps": self.max_slider.value(),
            "pauses_enabled": self.pauses_cb.isChecked(),
            "pause_intensity": self.pauses_slider.value()
        }
        try:
            with open("config.json", "w") as f:
                json.dump(data, f)
        except:
            pass
        event.accept()

    def update_parameters(self):
        min_val = self.min_slider.value()
        max_val = self.max_slider.value()
        pause_val = self.pauses_slider.value()
        pauses_active = self.pauses_cb.isChecked()

        if min_val >= max_val:
            min_val = max_val - 1
            self.min_slider.blockSignals(True)
            self.min_slider.setValue(min_val)
            self.min_slider.blockSignals(False)

        self.min_lbl.setText(f"Minimum CPS: {min_val}")
        self.max_lbl.setText(f"Maximum CPS: {max_val}")
        self.pauses_lbl.setText(f"Pause Frequency: {pause_val}")

        self.pauses_slider.setEnabled(pauses_active)
        self.pauses_lbl.setEnabled(pauses_active)

        self.controller.min_cps = min_val
        self.controller.max_cps = max_val
        self.controller.pause_intensity = pause_val
        self.controller.pauses_enabled = pauses_active

    def toggle_clicker(self, state):
        self.controller.clicker_enabled = (state == 2)

    def sync_ui_with_controller(self):
        if self.clicker_cb.isChecked() != self.controller.clicker_enabled:
            self.clicker_cb.blockSignals(True)
            self.clicker_cb.setChecked(self.controller.clicker_enabled)
            self.clicker_cb.blockSignals(False)

        if self.controller.clicker_enabled:
            self.status_lbl.setText("Status: ACTIVE")
            self.status_lbl.setStyleSheet("color: #28a745; font-weight: bold;")
        else:
            self.status_lbl.setText("Status: Idle")
            self.status_lbl.setStyleSheet("color: #212529;")

        self.clicks_lbl.setText(f"Session Clicks: {self.controller.session_clicks}")
