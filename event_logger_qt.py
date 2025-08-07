#!/usr/bin/env python3
"""
Qt Event Logger for TRBD Clinical Trial
Cross-platform desktop application with reliable audio feedback

@author Yewen
@version 1.0 08/07/2025
"""

import sys
import os
import csv
from datetime import datetime
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QVBoxLayout,
    QWidget,
    QPushButton,
    QLabel,
    QMessageBox,
    QGridLayout,
    QLineEdit,
    QFrame,
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont


class EventLogger(QMainWindow):
    def __init__(self, project_id=""):
        super().__init__()
        self.project_id = project_id
        self.current_event = None
        self.active_button = None
        self.active_events = {}
        self.event_buttons = {}

        # Setup data file
        self.setup_data_file()

        # Setup audio
        self.setup_audio()

        # Setup UI
        self.init_ui()

        # Show initial status
        self.update_status("Press a button to start an event")

    def setup_data_file(self):
        """Initialize CSV data file"""
        time_stamp = datetime.now().strftime("%m%d_%H_%M")
        output_folder = ""

        if self.project_id == "":
            self.data_file = os.path.join(output_folder, f"event_log_{time_stamp}.csv")
        else:
            self.data_file = os.path.join(
                output_folder, f"{self.project_id}_event_log_{time_stamp}.csv"
            )

        if not os.path.exists(self.data_file):
            with open(self.data_file, "w", newline="") as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(
                    [
                        "Event",
                        "Start Date",
                        "Start Time",
                        "End Date",
                        "End Time",
                        "Notes",
                    ]
                )

    def setup_audio(self):
        """Initialize audio system"""
        # Use system beep - most reliable and no files needed
        self.use_system_beep = True

    def play_beep(self):
        """Play audio feedback - guaranteed to work"""
        try:
            # Most reliable method - system beep
            QApplication.beep()
        except Exception as e:
            print(f"Audio playback error: {e}")

    def init_ui(self):
        """Initialize the user interface"""
        self.setWindowTitle("TRBD Event Logger")
        self.setGeometry(100, 100, 800, 600)

        # Create central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Main layout
        layout = QVBoxLayout(central_widget)
        layout.setSpacing(20)
        layout.setContentsMargins(20, 20, 20, 20)

        # Project ID display (if provided)
        if self.project_id:
            project_label = QLabel(f"Project ID: {self.project_id}")
            project_label.setFont(QFont("Arial", 12, QFont.Weight.Bold))
            project_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            project_label.setStyleSheet("QLabel { color: #2c3e50; padding: 10px; }")
            layout.addWidget(project_label)

        # Status display
        self.status_label = QLabel("Press a button to start an event")
        self.status_label.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status_label.setStyleSheet(
            """
            QLabel {
                background-color: #ecf0f1;
                color: #2c3e50;
                border: 2px solid #bdc3c7;
                border-radius: 10px;
                padding: 15px;
                min-height: 20px;
            }
        """
        )
        layout.addWidget(self.status_label)

        # Event buttons grid
        self.create_event_buttons(layout)

        # Controls section
        self.create_controls(layout)

        # Apply general styling
        self.setStyleSheet(
            """
            QMainWindow {
                background-color: #f8f9fa;
            }
            QPushButton {
                font-size: 14px;
                font-weight: bold;
                padding: 15px;
                border-radius: 10px;
                border: 2px solid transparent;
                min-height: 20px;
            }
        """
        )

    def create_event_buttons(self, layout):
        """Create the grid of event buttons"""
        # Button configuration - matching your original layout
        buttons_config = [
            ("DBS Programming Session", "#3498db", "#2980b9"),
            ("Clinical Interview", "#e74c3c", "#c0392b"),
            ("Lounge Activity", "#f39c12", "#e67e22"),
            ("Surprise", "#9b59b6", "#8e44ad"),
            ("VR-PAAT", "#1abc9c", "#16a085"),
            ("Sleep Period", "#34495e", "#2c3e50"),
            ("Meal", "#e67e22", "#d35400"),
            ("Social", "#27ae60", "#229954"),
            ("Break", "#f1c40f", "#f39c12"),
            ("Other", "#95a5a6", "#7f8c8d"),
        ]

        # Create grid layout for buttons
        button_frame = QFrame()
        button_layout = QGridLayout(button_frame)
        button_layout.setSpacing(15)

        # Arrange buttons in a 5x2 grid
        for i, (event_name, color, hover_color) in enumerate(buttons_config):
            row = i // 5
            col = i % 5

            button = QPushButton(event_name)
            button.clicked.connect(
                lambda checked, name=event_name, btn=button: self.toggle_event(
                    name, btn
                )
            )

            # Style the button
            button.setStyleSheet(
                f"""
                QPushButton {{
                    background-color: {color};
                    color: white;
                    border: 4px solid {color};
                }}
                QPushButton:hover {{
                    background-color: {hover_color};
                    border-color: {hover_color};
                }}
                QPushButton:pressed {{
                    background-color: {hover_color};
                }}
            """
            )

            self.event_buttons[event_name] = button
            button_layout.addWidget(button, row, col)

        layout.addWidget(button_frame)

    def create_controls(self, layout):
        """Create the notes input and abort button"""
        controls_frame = QFrame()
        controls_layout = QVBoxLayout(controls_frame)
        controls_layout.setSpacing(10)

        # Notes input
        notes_label = QLabel("Optional Notes (only while event active):")
        notes_label.setFont(QFont("Arial", 11))
        controls_layout.addWidget(notes_label)

        self.notes_input = QLineEdit()
        self.notes_input.setPlaceholderText("Enter optional notes...")
        self.notes_input.setFont(QFont("Arial", 12))
        self.notes_input.setStyleSheet(
            """
            QLineEdit {
                padding: 10px;
                border: 2px solid #bdc3c7;
                border-radius: 5px;
                font-size: 12px;
            }
            QLineEdit:focus {
                border-color: #3498db;
            }
        """
        )
        controls_layout.addWidget(self.notes_input)

        # Abort button
        self.abort_button = QPushButton("Abort Current Event")
        self.abort_button.clicked.connect(self.abort_event)
        self.abort_button.setStyleSheet(
            """
            QPushButton {
                background-color: #e74c3c;
                color: white;
                border: 3px solid #e74c3c;
                font-size: 16px;
                padding: 12px;
            }
            QPushButton:hover {
                background-color: #c0392b;
                border-color: #c0392b;
            }
            QPushButton:pressed {
                background-color: #a93226;
            }
        """
        )
        controls_layout.addWidget(self.abort_button)

        layout.addWidget(controls_frame)

    def update_status(self, message):
        """Update the status label"""
        self.status_label.setText(message)

    def toggle_event(self, event_name, button):
        """Toggle an event on/off"""
        notes = self.notes_input.text()

        if event_name in self.active_events:
            # End the event
            start_time = self.active_events.pop(event_name)
            self.log_event(event_name, start_time, datetime.now(), notes)

            # Update UI - restore original button style
            self.restore_button_style(button, event_name)
            self.current_event = None
            self.active_button = None
            self.notes_input.clear()
            self.update_status("Press a button to start an event")

        else:
            # Start new event (clear any existing events first)
            self.active_events.clear()

            # Deactivate previous button
            if self.active_button:
                for btn_name, btn in self.event_buttons.items():
                    if btn == self.active_button:
                        self.restore_button_style(btn, btn_name)
                        break

            # Start new event
            self.active_events[event_name] = datetime.now()

            # Update UI - set active style
            self.set_active_button_style(button)
            self.current_event = event_name
            self.active_button = button
            self.update_status(f"{event_name} has started")

        # Play audio feedback
        self.play_beep()

    def get_button_config(self, event_name):
        """Get the original color configuration for a button"""
        buttons_config = {
            "DBS Programming Session": ("#3498db", "#2980b9"),
            "Clinical Interview": ("#e74c3c", "#c0392b"),
            "Lounge Activity": ("#f39c12", "#e67e22"),
            "Surprise": ("#9b59b6", "#8e44ad"),
            "VR-PAAT": ("#1abc9c", "#16a085"),
            "Sleep Period": ("#34495e", "#2c3e50"),
            "Meal": ("#e67e22", "#d35400"),
            "Social": ("#27ae60", "#229954"),
            "Break": ("#f1c40f", "#f39c12"),
            "Other": ("#95a5a6", "#7f8c8d"),
        }
        return buttons_config.get(event_name, ("#95a5a6", "#7f8c8d"))

    def restore_button_style(self, button, event_name):
        """Restore button to its original style"""
        color, hover_color = self.get_button_config(event_name)
        button.setStyleSheet(
            f"""
            QPushButton {{
                background-color: {color};
                color: white;
                border: 4px solid {color};
            }}
            QPushButton:hover {{
                background-color: {hover_color};
                border-color: {hover_color};
            }}
            QPushButton:pressed {{
                background-color: {hover_color};
            }}
        """
        )

    def set_active_button_style(self, button):
        """Set button to active (green) style"""
        button.setStyleSheet(
            """
            QPushButton {
                background-color: #2ecc71 !important;
                color: white !important;
                border: 4px solid #27ae60 !important;
            }
            QPushButton:hover {
                background-color: #27ae60 !important;
                border-color: #27ae60 !important;
            }
            QPushButton:pressed {
                background-color: #27ae60 !important;
            }
        """
        )

    def abort_event(self):
        """Abort the current active event"""
        if not self.active_events:
            QMessageBox.information(
                self, "No Active Event", "No active event to abort."
            )
            return

        notes = self.notes_input.text()
        event_name = next(iter(self.active_events))
        start_time = self.active_events.pop(event_name)

        # Add ABORTED prefix to notes
        abort_notes = f"ABORTED: {notes}" if notes else "ABORTED"

        # Log the aborted event (no end time)
        self.log_event(event_name, start_time, None, abort_notes)

        # Update UI
        if self.active_button:
            self.restore_button_style(self.active_button, event_name)

        self.current_event = None
        self.active_button = None
        self.notes_input.clear()
        self.update_status("Event Aborted")

        # Play audio feedback
        self.play_beep()

    def log_event(self, event_name, start_time, end_time, notes=""):
        """Log an event to the CSV file"""
        end_date = end_time.strftime("%Y-%m-%d") if end_time else "N/A"
        end_time_str = end_time.strftime("%H:%M:%S") if end_time else "N/A"

        data = [
            event_name,
            start_time.strftime("%Y-%m-%d"),
            start_time.strftime("%H:%M:%S"),
            end_date,
            end_time_str,
            notes,
        ]

        with open(self.data_file, "a", newline="") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(data)

        print(f"Logged event to {os.path.abspath(self.data_file)}:")
        print(f"  Event: {event_name}")
        print(f"  Start: {start_time}")
        print(f"  End: {end_time}")
        print(f"  Notes: {notes}")

    def closeEvent(self, event):
        """Handle application close"""
        if self.active_events:
            reply = QMessageBox.question(
                self,
                "Active Event",
                "There is an active event. Do you want to abort it before closing?",
                QMessageBox.StandardButton.Yes
                | QMessageBox.StandardButton.No
                | QMessageBox.StandardButton.Cancel,
            )

            if reply == QMessageBox.StandardButton.Yes:
                self.abort_event()
                event.accept()
            elif reply == QMessageBox.StandardButton.No:
                event.accept()
            else:
                event.ignore()
        else:
            event.accept()


def main():
    app = QApplication(sys.argv)

    # Set application properties
    app.setApplicationName("TRBD Event Logger")
    app.setApplicationVersion("2.0")
    app.setOrganizationName("Baylor College of Medicine")

    # Get project ID from command line
    project_id = ""
    if len(sys.argv) >= 2:
        project_id = sys.argv[1]

    # Create and show the main window
    window = EventLogger(project_id)
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
