#!/usr/bin/env python3
"""
Unified Event Logger for TRBD Clinical Trial
Supports multiple deployment configurations (Jamail, NBU)
Cross-platform desktop application with reliable audio feedback

@author Yewen
@version 2.0 02/18/2026
"""

import sys
import os
import csv
import subprocess
from datetime import datetime
from pathlib import Path

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
    QHBoxLayout,
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

# Import from our modules
from config import AppConfig, CONFIGS
from constants import (
    CSV_HEADERS,
    MAIN_WINDOW_SIZE,
    BUTTON_GRID_COLUMNS,
    BUTTON_GRID_SPACING,
    DEFAULT_FONT_FAMILY,
)
from styles import (
    MAIN_WINDOW_STYLE,
    PROJECT_ID_STYLE,
    STATUS_LABEL_STYLE,
    EVENT_BUTTON_NORMAL_STYLE,
    EVENT_BUTTON_ACTIVE_STYLE,
    EVENT_BUTTON_DISABLED_STYLE,
    CONTROLS_FRAME_STYLE,
    NOTES_INPUT_STYLE,
    ABORT_BUTTON_STYLE,
    MISSING_EVENTS_BUTTON_STYLE,
    END_SESSION_BUTTON_STYLE,
    MESSAGE_BOX_INFO_STYLE,
    MESSAGE_BOX_WARNING_STYLE,
    MESSAGE_BOX_QUESTION_STYLE,
)
from dialogs import ConfigSelectionDialog, StartupDialog, MissingEventDialog
from utils import (
    calculate_duration,
    log_to_csv,
    show_info_message,
    show_warning_message,
    show_question_message,
    get_current_date_folder,
    format_datetime_for_display,
)


class EventLogger(QMainWindow):
    """Main event logger application window"""
    
    def __init__(self, config, patient_id="", record_session_start=False):
        super().__init__()
        self.config = config
        self.patient_id = patient_id
        self.current_event = None
        self.active_button = None
        self.active_events = {}
        self.event_buttons = {}
        self.session_start_time = None
        self.run_parser = config.run_parser

        # Get study ID from patient ID if provided
        if patient_id:
            self.study_id = config.get_study_id(patient_id)
        else:
            self.study_id = "DefaultStudy"

        # Setup data file
        self.setup_data_file()

        # Record session start if requested
        if record_session_start:
            self.record_session_start()

        # Setup audio
        self.setup_audio()

        # Setup UI
        self.init_ui()

        # Show initial status
        self.update_status("Press a button to start an event")

    def setup_data_file(self):
        """Initialize CSV data file and directory"""
        date_folder = get_current_date_folder()

        # Use configured root path or ask for patient directory
        if self.patient_id and self.config.root_path:
            # Use structured path: ROOT/StudyID/PatientID/Date
            root_path = self.config.root_path / self.study_id / self.patient_id
        else:
            # Ask user to select directory
            selected_path = QFileDialog.getExistingDirectory(
                None, "Select patient folder to save event logs"
            )
            if selected_path:
                root_path = Path(selected_path)
            else:
                root_path = Path(os.getcwd())  # Fallback

        # Create date sub-directory if it doesn't exist
        folder_path = root_path / date_folder
        folder_path.mkdir(parents=True, exist_ok=True)

        # Get filename with timestamp (including seconds to avoid collisions)
        filename = datetime.now().strftime("event_log_%m%d_%H_%M_%S.csv")
        
        # Add patient ID prefix if provided
        if self.patient_id:
            filename = f"{self.patient_id}_{filename}"

        self.data_file = os.path.join(folder_path, filename)

        # Create CSV file with headers
        if not os.path.exists(self.data_file):
            with open(self.data_file, "w", newline="") as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(CSV_HEADERS)

    def record_session_start(self):
        """Record session start time to CSV"""
        self.session_start_time = datetime.now()
        with open(self.data_file, "a", newline="") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([
                "SESSION START",
                self.session_start_time.strftime("%Y-%m-%d"),
                self.session_start_time.strftime("%H:%M:%S"),
                "N/A",
                "N/A",
                "Session started"
            ])
        print(f"Session started at: {format_datetime_for_display(self.session_start_time)}")

    def setup_audio(self):
        """Initialize audio system"""
        # Use system beep - most reliable and no files needed
        self.use_system_beep = True

    def play_beep(self):
        """Play audio feedback - guaranteed to work"""
        try:
            QApplication.beep()
        except Exception as e:
            print(f"Audio playback error: {e}")

    def init_ui(self):
        """Initialize the user interface"""
        self.setWindowTitle(self.config.app_name)
        self.setGeometry(100, 100, *MAIN_WINDOW_SIZE)

        # Create central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Main layout
        layout = QVBoxLayout(central_widget)
        layout.setSpacing(25)
        layout.setContentsMargins(30, 30, 30, 30)

        # Patient ID display (if provided)
        if self.patient_id:
            patient_label = QLabel(f"👤 Patient ID: {self.patient_id} | Study: {self.study_id}")
            patient_label.setFont(QFont(DEFAULT_FONT_FAMILY, 12, QFont.Weight.Bold))
            patient_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            patient_label.setStyleSheet(PROJECT_ID_STYLE)
            layout.addWidget(patient_label)

        # Configuration indicator
        config_label = QLabel(f"⚙️ Configuration: {self.config.config_name}")
        config_label.setFont(QFont(DEFAULT_FONT_FAMILY, 10))
        config_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        config_label.setStyleSheet("QLabel { color: #7f8c8d; padding: 5px; }")
        layout.addWidget(config_label)

        # Status display
        self.status_label = QLabel("Press a button to start an event")
        self.status_label.setFont(QFont(DEFAULT_FONT_FAMILY, 15, QFont.Weight.Bold))
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status_label.setStyleSheet(STATUS_LABEL_STYLE)
        layout.addWidget(self.status_label)

        # Event buttons grid
        self.create_event_buttons(layout)

        # Controls section
        self.create_controls(layout)

        # Apply general styling
        self.setStyleSheet(MAIN_WINDOW_STYLE)

    def create_event_buttons(self, layout):
        """Create the grid of event buttons from configuration"""
        # Create grid layout for buttons
        button_frame = QFrame()
        button_frame.setStyleSheet("QFrame { background-color: transparent; }")
        button_layout = QGridLayout(button_frame)
        button_layout.setSpacing(BUTTON_GRID_SPACING)

        # Get events from configuration
        events = self.config.events

        # Arrange buttons in a grid
        for i, (display_name, event_name) in enumerate(events):
            row = i // BUTTON_GRID_COLUMNS
            col = i % BUTTON_GRID_COLUMNS

            button = QPushButton(display_name)
            button.setFont(QFont(DEFAULT_FONT_FAMILY, 12, QFont.Weight.DemiBold))
            button.clicked.connect(
                lambda checked, name=event_name, btn=button: self.toggle_event(name, btn)
            )
            button.setStyleSheet(EVENT_BUTTON_NORMAL_STYLE)

            self.event_buttons[event_name] = button
            button_layout.addWidget(button, row, col)

        layout.addWidget(button_frame)

    def create_controls(self, layout):
        """Create the notes input and control buttons"""
        controls_frame = QFrame()
        controls_frame.setStyleSheet(CONTROLS_FRAME_STYLE)
        controls_layout = QVBoxLayout(controls_frame)
        controls_layout.setSpacing(15)
        controls_layout.setContentsMargins(20, 20, 20, 20)

        # Notes input
        notes_label = QLabel("📝 Optional Notes (only while event active):")
        notes_label.setFont(QFont(DEFAULT_FONT_FAMILY, 11, QFont.Weight.DemiBold))
        notes_label.setStyleSheet("QLabel { color: #34495e; }")
        controls_layout.addWidget(notes_label)

        self.notes_input = QLineEdit()
        self.notes_input.setPlaceholderText("Enter optional notes...")
        self.notes_input.setFont(QFont(DEFAULT_FONT_FAMILY, 11))
        self.notes_input.setStyleSheet(NOTES_INPUT_STYLE)
        controls_layout.addWidget(self.notes_input)

        # Buttons layout (horizontal)
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(12)

        # Abort button
        self.abort_button = QPushButton("⚠️ Abort Current Event")
        self.abort_button.setFont(QFont(DEFAULT_FONT_FAMILY, 12, QFont.Weight.Bold))
        self.abort_button.clicked.connect(self.abort_event)
        self.abort_button.setStyleSheet(ABORT_BUTTON_STYLE)
        buttons_layout.addWidget(self.abort_button)

        # Missing Events button
        self.missing_event_button = QPushButton("➕ Add Missing Events")
        self.missing_event_button.setFont(QFont(DEFAULT_FONT_FAMILY, 12, QFont.Weight.Bold))
        self.missing_event_button.clicked.connect(self.open_missing_event_dialog)
        self.missing_event_button.setStyleSheet(MISSING_EVENTS_BUTTON_STYLE)
        buttons_layout.addWidget(self.missing_event_button)

        controls_layout.addLayout(buttons_layout)
        layout.addWidget(controls_frame)

        # End Session button at the bottom
        self.end_session_button = QPushButton("🔚 End Session and Close")
        self.end_session_button.setFont(QFont(DEFAULT_FONT_FAMILY, 14, QFont.Weight.Bold))
        self.end_session_button.clicked.connect(self.end_session)
        self.end_session_button.setStyleSheet(END_SESSION_BUTTON_STYLE)
        layout.addWidget(self.end_session_button)

    def update_status(self, message):
        """Update the status label"""
        self.status_label.setText(message)

    def end_session(self):
        """End the session, record end time, and close the application"""
        end_time = datetime.now()
        
        # Calculate duration
        duration_str = calculate_duration(self.session_start_time, end_time)
        end_message = f"Session ended at: {format_datetime_for_display(end_time)}"
        
        # If there are active events, ask to abort them
        if self.active_events:
            msg_box = QMessageBox(self)
            msg_box.setIcon(QMessageBox.Icon.Question)
            msg_box.setWindowTitle("Active Event")
            msg_box.setText("There is an active event. Do you want to abort it before ending the session?")
            msg_box.setStandardButtons(
                QMessageBox.StandardButton.Yes | 
                QMessageBox.StandardButton.No | 
                QMessageBox.StandardButton.Cancel
            )
            msg_box.setStyleSheet(MESSAGE_BOX_QUESTION_STYLE)
            reply = msg_box.exec()
            
            if reply == QMessageBox.StandardButton.Cancel:
                return
            elif reply == QMessageBox.StandardButton.Yes:
                self.abort_event()
        
        # Write end session marker to CSV
        with open(self.data_file, "a", newline="") as csvfile:
            writer = csv.writer(csvfile)
            if self.session_start_time:
                writer.writerow([
                    "SESSION END",
                    self.session_start_time.strftime("%Y-%m-%d"),
                    self.session_start_time.strftime("%H:%M:%S"),
                    end_time.strftime("%Y-%m-%d"),
                    end_time.strftime("%H:%M:%S"),
                    f"Session ended, duration: {duration_str}"
                ])
            else:
                writer.writerow([
                    "SESSION END",
                    "N/A",
                    "N/A",
                    end_time.strftime("%Y-%m-%d"),
                    end_time.strftime("%H:%M:%S"),
                    "Session ended, duration: N/A (session start not recorded)"
                ])
        
        print(end_message)
        print(f"Total session duration: {duration_str}")
        
        # Show confirmation and close
        if self.session_start_time:
            message_text = f"{end_message}\nDuration: {duration_str}\n\nThe application will now close."
        else:
            message_text = f"{end_message}\nDuration: N/A (session start not recorded)\n\nThe application will now close."
        
        show_info_message(self, "Session Ended", message_text)
        QApplication.instance().quit()

    def disable_all_buttons_except(self, active_button):
        """Disable all event buttons except the active one"""
        for button in self.event_buttons.values():
            if button != active_button:
                button.setEnabled(False)
                button.setStyleSheet(EVENT_BUTTON_DISABLED_STYLE)
        
        # Also disable the missing events button
        self.missing_event_button.setEnabled(False)

    def enable_all_buttons(self):
        """Enable all event buttons and restore normal style"""
        for button in self.event_buttons.values():
            button.setEnabled(True)
            button.setStyleSheet(EVENT_BUTTON_NORMAL_STYLE)
        
        # Also enable the missing events button
        self.missing_event_button.setEnabled(True)

    def open_missing_event_dialog(self):
        """Open dialog for entering missing events"""
        # Pass event options from configuration
        dialog = MissingEventDialog(
            self, 
            submit_callback=self.submit_missing_event,
            event_options=self.config.event_display_names
        )
        dialog.exec()

    def submit_missing_event(self, event_name, start_qtime, end_qtime, user_notes=""):
        """Submit missing event to CSV"""
        # Get current date
        current_date = datetime.now().strftime("%Y-%m-%d")

        # Convert QTime to strings
        start_time_str = start_qtime.toString("HH:mm:ss")
        end_time_str = end_qtime.toString("HH:mm:ss")

        # Create datetime objects for logging
        start_datetime = datetime.strptime(f"{current_date} {start_time_str}", "%Y-%m-%d %H:%M:%S")
        end_datetime = datetime.strptime(f"{current_date} {end_time_str}", "%Y-%m-%d %H:%M:%S")

        # Combine "Missing event" with user notes
        notes = "Missing event"
        if user_notes.strip():
            notes += f": {user_notes.strip()}"

        # Log the event
        self.log_event(event_name, start_datetime, end_datetime, notes)

        # Play beep feedback
        self.play_beep()
        
        return True  # Indicate success

    def toggle_event(self, event_name, button):
        """Toggle an event on/off"""
        notes = self.notes_input.text()

        if event_name in self.active_events:
            # End the event
            start_time = self.active_events.pop(event_name)
            self.log_event(event_name, start_time, datetime.now(), notes)

            # Update UI - restore original button style
            button.setStyleSheet(EVENT_BUTTON_NORMAL_STYLE)
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
                self.active_button.setStyleSheet(EVENT_BUTTON_NORMAL_STYLE)

            # Start new event
            self.active_events[event_name] = datetime.now()

            # Update UI - set active style
            button.setStyleSheet(EVENT_BUTTON_ACTIVE_STYLE)
            self.current_event = event_name
            self.active_button = button
            self.disable_all_buttons_except(button)
            self.update_status(f"{event_name} has started")

        # Play audio feedback
        self.play_beep()

    def abort_event(self):
        """Abort the current active event"""
        if not self.active_events:
            show_info_message(self, "No Active Event", "No active event to abort.")
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
            self.active_button.setStyleSheet(EVENT_BUTTON_NORMAL_STYLE)

        self.current_event = None
        self.active_button = None
        self.notes_input.clear()
        self.enable_all_buttons()
        self.update_status("Event Aborted")

        # Play audio feedback
        self.play_beep()

    def log_event(self, event_name, start_time, end_time, notes=""):
        """Log an event to the CSV file"""
        log_to_csv(self.data_file, event_name, start_time, end_time, notes)

    def closeEvent(self, event):
        """Handle application close"""
        if self.active_events:
            msg_box = QMessageBox(self)
            msg_box.setIcon(QMessageBox.Icon.Question)
            msg_box.setWindowTitle("Active Event")
            msg_box.setText("There is an active event. Do you want to abort it before closing?")
            msg_box.setStandardButtons(
                QMessageBox.StandardButton.Yes | 
                QMessageBox.StandardButton.No | 
                QMessageBox.StandardButton.Cancel
            )
            msg_box.setStyleSheet(MESSAGE_BOX_QUESTION_STYLE)
            reply = msg_box.exec()

            if reply == QMessageBox.StandardButton.Cancel:
                event.ignore()
                return
            elif reply == QMessageBox.StandardButton.Yes:
                self.abort_event()

        event.accept()


def main():
    """Main application entry point"""
    app = QApplication(sys.argv)

    # Set application properties
    app.setApplicationName("Event Logger")
    app.setApplicationVersion("2.0")
    app.setOrganizationName("Baylor College of Medicine")

    # Step 1: Select configuration
    config_dialog = ConfigSelectionDialog()
    if config_dialog.exec() != QDialog.DialogCode.Accepted:
        sys.exit(0)
    
    selected_config_name = config_dialog.selected_config
    config = AppConfig(selected_config_name)

    # Get patient ID from command line if provided
    patient_id = ""
    if len(sys.argv) >= 2:
        patient_id = sys.argv[1]

    # Step 2: Show startup dialog for session start recording
    startup_dialog = StartupDialog(app_name=config.app_name)
    if startup_dialog.exec() != QDialog.DialogCode.Accepted:
        sys.exit(0)

    # Get whether to record session start (or use config default)
    record_start = startup_dialog.record_start or config.record_start_time

    # Step 3: Create and show the main window
    window = EventLogger(config, patient_id, record_start)
    window.show()

    # Run the Qt event loop and capture its exit code
    exit_code = app.exec()

    # Step 4: Run source parser if configured (NBU only)
    if getattr(window, "run_parser", False) and config.parser_path:
        print(f"\nRunning source parser: {config.parser_path}")
        try:
            result = subprocess.run(
                config.parser_path,
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                shell=True
            )
            print("✓ Logger source parser completed successfully")
            print("  Check Elias for processed files")
        except subprocess.CalledProcessError as e:
            print("✗ Error running logger source parser")
            print(f"  STDOUT: {e.stdout}")
            print(f"  STDERR: {e.stderr}")
        except Exception as e:
            print(f"✗ Unexpected error: {e}")

    # Exit with the same code returned by the Qt event loop
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
