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
    QFileDialog,
    QDialog,
    QComboBox,
    QTimeEdit,
    QHBoxLayout,
)
from PyQt6.QtCore import Qt, QTime
from PyQt6.QtGui import QFont
from pathlib import Path


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
        """Initialize CSV data file and directory"""
        date = datetime.now().strftime("%Y-%m-%d")

        # Patient directory selection
        root_path = QFileDialog.getExistingDirectory(
            None, "Select patient folder to save event logs"
        )

        if root_path == "" or root_path is None:
            root_path = Path(os.getcwd())  # Fallback to current working directory

        # Create date sub-directory if it doesn't exist
        folder_path = Path(root_path) / date
        if not folder_path.exists():
            folder_path.mkdir(parents=True, exist_ok=True)

        time_stamp = datetime.now().strftime("%m%d_%H_%M")
        output_folder = folder_path

        # Create data file
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
        # Button configuration - all buttons start with same blue color
        buttons_config = [
            "DBS Programming Session",
            "Clinical Interview",
            "Lounge Activity",
            "Surprise",
            "VR-PAAT",
            "Sleep Period",
            "Meal",
            "Social",
            "Break",
            "IPG Charging",
            "CTM Disconnect",
            "Walk",
            "Snack",
            "Resting state",
            "Other",
        ]

        # Create grid layout for buttons
        button_frame = QFrame()
        button_layout = QGridLayout(button_frame)
        button_layout.setSpacing(15)

        # Arrange buttons in a 5x3 grid
        for i, event_name in enumerate(buttons_config):
            row = i // 5
            col = i % 5

            button = QPushButton(event_name)
            button.clicked.connect(
                lambda checked, name=event_name, btn=button: self.toggle_event(
                    name, btn
                )
            )

            # Style the button - all start with blue color
            button.setStyleSheet(
                """
                QPushButton {
                    background-color: #3498db;
                    color: white;
                    border: 4px solid #3498db;
                }
                QPushButton:hover {
                    background-color: #2980b9;
                    border-color: #2980b9;
                }
                QPushButton:pressed {
                    background-color: #2980b9;
                }
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

        # Missing Events button
        self.missing_event_button = QPushButton("Add Missing Events")
        self.missing_event_button.clicked.connect(self.open_missing_event_dialog)
        self.missing_event_button.setStyleSheet(
            """
            QPushButton {
                background-color: #3498db;
                color: white;
                border: 3px solid #3498db;
                font-size: 16px;
                padding: 12px;
            }
            QPushButton:hover {
                background-color: #2980b9;
                border-color: #2980b9;
            }
            QPushButton:pressed {
                background-color: #2471a3;
            }
        """
        )
        controls_layout.addWidget(self.missing_event_button)

        layout.addWidget(controls_frame)

    def update_status(self, message):
        """Update the status label"""
        self.status_label.setText(message)

    def disable_all_buttons_except(self, active_button):
        """Disable all event buttons except the active one and set them to gray"""
        for button in self.event_buttons.values():
            if button != active_button:
                button.setEnabled(False)
                button.setStyleSheet(
                    """
                    QPushButton {
                        background-color: #95a5a6;
                        color: white;
                        border: 4px solid #95a5a6;
                    }
                """
                )

    def enable_all_buttons(self):
        """Enable all event buttons and restore blue color"""
        for button in self.event_buttons.values():
            button.setEnabled(True)
            button.setStyleSheet(
                """
                QPushButton {
                    background-color: #3498db;
                    color: white;
                    border: 4px solid #3498db;
                }
                QPushButton:hover {
                    background-color: #2980b9;
                    border-color: #2980b9;
                }
                QPushButton:pressed {
                    background-color: #2980b9;
                }
            """
            )

    def open_missing_event_dialog(self):
        """Open dialog for entering missing events"""
        dialog = QDialog(self)
        dialog.setWindowTitle("Add Missing Event")
        dialog.setModal(True)
        dialog.setMinimumWidth(400)

        layout = QVBoxLayout(dialog)
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)

        # Title
        title_label = QLabel("Enter Missing Event Details")
        title_label.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title_label)

        # Event selection
        event_label = QLabel("Select Event:")
        event_label.setFont(QFont("Arial", 11))
        layout.addWidget(event_label)

        event_combo = QComboBox()
        event_combo.addItems([
            "DBS Programming Session",
            "Clinical Interview",
            "Lounge Activity",
            "Surprise",
            "VR-PAAT",
            "Sleep Period",
            "Meal",
            "Social",
            "Break",
            "IPG Charging",
            "CTM Disconnect",
            "Walk",
            "Snack",
            "Resting state",
            "Other",
        ])
        event_combo.setFont(QFont("Arial", 11))
        event_combo.setStyleSheet(
            """
            QComboBox {
                padding: 8px;
                border: 2px solid #bdc3c7;
                border-radius: 5px;
            }
            QComboBox:focus {
                border-color: #3498db;
            }
        """
        )
        layout.addWidget(event_combo)

        # Start time
        start_label = QLabel("Start Time:")
        start_label.setFont(QFont("Arial", 11))
        layout.addWidget(start_label)

        start_time_edit = QTimeEdit()
        start_time_edit.setDisplayFormat("HH:mm:ss")
        start_time_edit.setTime(QTime.currentTime())
        start_time_edit.setFont(QFont("Arial", 11))
        start_time_edit.setStyleSheet(
            """
            QTimeEdit {
                padding: 8px;
                border: 2px solid #bdc3c7;
                border-radius: 5px;
            }
            QTimeEdit:focus {
                border-color: #3498db;
            }
        """
        )
        layout.addWidget(start_time_edit)

        # End time
        end_label = QLabel("End Time:")
        end_label.setFont(QFont("Arial", 11))
        layout.addWidget(end_label)

        end_time_edit = QTimeEdit()
        end_time_edit.setDisplayFormat("HH:mm:ss")
        end_time_edit.setTime(QTime.currentTime())
        end_time_edit.setFont(QFont("Arial", 11))
        end_time_edit.setStyleSheet(
            """
            QTimeEdit {
                padding: 8px;
                border: 2px solid #bdc3c7;
                border-radius: 5px;
            }
            QTimeEdit:focus {
                border-color: #3498db;
            }
        """
        )
        layout.addWidget(end_time_edit)

        # Optional notes
        notes_label = QLabel("Optional Notes:")
        notes_label.setFont(QFont("Arial", 11))
        layout.addWidget(notes_label)

        notes_input = QLineEdit()
        notes_input.setPlaceholderText("Enter optional notes...")
        notes_input.setFont(QFont("Arial", 11))
        notes_input.setStyleSheet(
            """
            QLineEdit {
                padding: 8px;
                border: 2px solid #bdc3c7;
                border-radius: 5px;
            }
            QLineEdit:focus {
                border-color: #3498db;
            }
        """
        )
        layout.addWidget(notes_input)

        # Buttons
        button_layout = QHBoxLayout()
        button_layout.setSpacing(10)

        submit_button = QPushButton("Submit")
        submit_button.setFont(QFont("Arial", 11, QFont.Weight.Bold))
        submit_button.setStyleSheet(
            """
            QPushButton {
                background-color: #27ae60;
                color: white;
                border: 2px solid #27ae60;
                border-radius: 5px;
                padding: 10px 20px;
            }
            QPushButton:hover {
                background-color: #229954;
                border-color: #229954;
            }
        """
        )
        submit_button.clicked.connect(
            lambda: self.submit_missing_event(
                dialog,
                event_combo.currentText(),
                start_time_edit.time(),
                end_time_edit.time(),
                notes_input.text(),
            )
        )
        button_layout.addWidget(submit_button)

        cancel_button = QPushButton("Cancel")
        cancel_button.setFont(QFont("Arial", 11, QFont.Weight.Bold))
        cancel_button.setStyleSheet(
            """
            QPushButton {
                background-color: #95a5a6;
                color: white;
                border: 2px solid #95a5a6;
                border-radius: 5px;
                padding: 10px 20px;
            }
            QPushButton:hover {
                background-color: #7f8c8d;
                border-color: #7f8c8d;
            }
        """
        )
        cancel_button.clicked.connect(dialog.reject)
        button_layout.addWidget(cancel_button)

        layout.addLayout(button_layout)

        dialog.exec()

    def submit_missing_event(self, dialog, event_name, start_qtime, end_qtime, user_notes=""):
        """Submit missing event to CSV"""
        # Get current date
        current_date = datetime.now().strftime("%Y-%m-%d")

        # Convert QTime to strings
        start_time_str = start_qtime.toString("HH:mm:ss")
        end_time_str = end_qtime.toString("HH:mm:ss")

        # Validate that end time is after start time
        if end_qtime <= start_qtime:
            QMessageBox.warning(
                dialog,
                "Invalid Time Range",
                "End time must be after start time.",
            )
            return

        # Create datetime objects for logging
        start_datetime = datetime.strptime(
            f"{current_date} {start_time_str}", "%Y-%m-%d %H:%M:%S"
        )
        end_datetime = datetime.strptime(
            f"{current_date} {end_time_str}", "%Y-%m-%d %H:%M:%S"
        )

        # Combine "Missing event" with user notes
        notes = "Missing event"
        if user_notes.strip():
            notes += f": {user_notes.strip()}"

        # Log the event
        self.log_event(event_name, start_datetime, end_datetime, notes)

        # Show confirmation
        QMessageBox.information(
            dialog,
            "Success",
            f"Missing event '{event_name}' has been logged successfully.",
        )

        # Play beep feedback
        self.play_beep()

        # Close dialog
        dialog.accept()

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
            self.enable_all_buttons()
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
            self.disable_all_buttons_except(button)
            self.update_status(f"{event_name} has started")

        # Play audio feedback
        self.play_beep()

    def restore_button_style(self, button, event_name):
        """Restore button to its original blue style"""
        button.setStyleSheet(
            """
            QPushButton {
                background-color: #3498db;
                color: white;
                border: 4px solid #3498db;
            }
            QPushButton:hover {
                background-color: #2980b9;
                border-color: #2980b9;
            }
            QPushButton:pressed {
                background-color: #2980b9;
            }
        """
        )

    def set_active_button_style(self, button):
        """Set button to active (teal) style"""
        button.setStyleSheet(
            """
            QPushButton {
                background-color: #1abc9c !important;
                color: white !important;
                border: 4px solid #1abc9c !important;
            }
            QPushButton:hover {
                background-color: #16a085 !important;
                border-color: #16a085 !important;
            }
            QPushButton:pressed {
                background-color: #16a085 !important;
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
        self.enable_all_buttons()
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
