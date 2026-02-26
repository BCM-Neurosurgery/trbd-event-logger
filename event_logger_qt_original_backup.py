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


class StartupDialog(QDialog):
    """Startup dialog for session initialization"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.record_start = False
        self.init_ui()

    def init_ui(self):
        """Initialize the startup dialog UI"""
        self.setWindowTitle("TRBD Event Logger - Session Start")
        self.setModal(True)
        self.setMinimumWidth(600)
        self.setMinimumHeight(350)

        layout = QVBoxLayout(self)
        layout.setSpacing(30)
        layout.setContentsMargins(40, 40, 40, 40)

        # Title
        title_label = QLabel("🏥 Welcome to TRBD Event Logger")
        title_label.setFont(QFont("Segoe UI", 20, QFont.Weight.Bold))
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet(
            """
            QLabel { 
                color: #2c3e50; 
                padding: 15px;
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #e8f4f8, stop:1 #d5e9f2);
                border-radius: 10px;
            }
            """
        )
        layout.addWidget(title_label)

        # Subtitle
        subtitle_label = QLabel("Do you want to record the session start time?")
        subtitle_label.setFont(QFont("Segoe UI", 14))
        subtitle_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle_label.setStyleSheet("QLabel { color: #34495e; padding: 15px; }")
        layout.addWidget(subtitle_label)

        # Spacer
        layout.addStretch()

        # Buttons layout
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(20)

        # Record Session Start button
        record_button = QPushButton("✅ Record Session Start")
        record_button.setFont(QFont("Segoe UI", 14, QFont.Weight.Bold))
        record_button.setMinimumHeight(70)
        record_button.setStyleSheet(
            """
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #2ecc71, stop:1 #27ae60);
                color: white;
                border: none;
                border-radius: 12px;
                padding: 18px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #58d68d, stop:1 #2ecc71);
            }
            QPushButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #27ae60, stop:1 #229954);
            }
        """
        )
        record_button.clicked.connect(self.record_and_continue)
        buttons_layout.addWidget(record_button)

        # Skip button
        skip_button = QPushButton("⏭️ Skip")
        skip_button.setFont(QFont("Segoe UI", 14, QFont.Weight.Bold))
        skip_button.setMinimumHeight(70)
        skip_button.setStyleSheet(
            """
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #bdc3c7, stop:1 #95a5a6);
                color: white;
                border: none;
                border-radius: 12px;
                padding: 18px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #d5dbdb, stop:1 #bdc3c7);
            }
            QPushButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #95a5a6, stop:1 #7f8c8d);
            }
        """
        )
        skip_button.clicked.connect(self.skip_and_continue)
        buttons_layout.addWidget(skip_button)

        layout.addLayout(buttons_layout)
        layout.addStretch()

        # Apply general styling
        self.setStyleSheet(
            """
            QDialog {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #f8f9fa, stop:1 #e9ecef);
            }
        """
        )

    def record_and_continue(self):
        """Record session start and continue to main window"""
        self.record_start = True
        self.accept()

    def skip_and_continue(self):
        """Skip recording and continue to main window"""
        self.record_start = False
        self.accept()


class EventLogger(QMainWindow):
    def __init__(self, project_id="", record_session_start=False):
        super().__init__()
        self.project_id = project_id
        self.current_event = None
        self.active_button = None
        self.active_events = {}
        self.event_buttons = {}
        self.session_start_time = None

        # Setup data file
        self.setup_data_file()

        # Record session start if requested
        if record_session_start:
            self.record_session_start()
        # If not recording, session_start_time remains None

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
        print(f"Session started at: {self.session_start_time.strftime('%Y-%m-%d %H:%M:%S')}")

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
        self.setGeometry(100, 100, 1000, 700)

        # Create central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Main layout
        layout = QVBoxLayout(central_widget)
        layout.setSpacing(25)
        layout.setContentsMargins(30, 30, 30, 30)

        # Project ID display (if provided)
        if self.project_id:
            project_label = QLabel(f"📋 Project ID: {self.project_id}")
            project_label.setFont(QFont("Segoe UI", 13, QFont.Weight.Bold))
            project_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            project_label.setStyleSheet(
                """
                QLabel { 
                    color: #2c3e50; 
                    padding: 12px;
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                        stop:0 #e8f4f8, stop:1 #d5e9f2);
                    border-radius: 8px;
                    border: 1px solid #b8d4e0;
                }
                """
            )
            layout.addWidget(project_label)

        # Status display
        self.status_label = QLabel("Press a button to start an event")
        self.status_label.setFont(QFont("Segoe UI", 15, QFont.Weight.Bold))
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status_label.setStyleSheet(
            """
            QLabel {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #ffffff, stop:1 #f5f7fa);
                color: #34495e;
                border: 2px solid #d5dce3;
                border-radius: 12px;
                padding: 20px;
                min-height: 30px;
                box-shadow: 0 2px 8px rgba(0,0,0,0.1);
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
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #f8f9fa, stop:1 #e9ecef);
            }
            QPushButton {
                font-size: 13px;
                font-weight: 600;
                padding: 15px;
                border-radius: 12px;
                border: none;
                min-height: 25px;
            }
        """
        )

    def create_event_buttons(self, layout):
        """Create the grid of event buttons"""
        # Button configuration with emojis
        buttons_config = [
            ("🧠 DBS Programming", "DBS Programming Session"),
            ("💬 Clinical Interview", "Clinical Interview"),
            ("🛋️ Lounge Activity", "Lounge Activity"),
            ("🎉 Surprise", "Surprise"),
            ("🥽 VR-PAAT", "VR-PAAT"),
            ("😴 Sleep Period", "Sleep Period"),
            ("🍽️ Meal", "Meal"),
            ("👥 Social", "Social"),
            ("☕ Break", "Break"),
            ("🔌 IPG Charging", "IPG Charging"),
            ("📡 CTM Disconnect", "CTM Disconnect"),
            ("🚶 Walk", "Walk"),
            ("🍿 Snack", "Snack"),
            ("🧘 Resting State", "Resting state"),
            ("📝 Other", "Other"),
        ]

        # Create grid layout for buttons
        button_frame = QFrame()
        button_frame.setStyleSheet(
            """
            QFrame {
                background-color: transparent;
            }
        """
        )
        button_layout = QGridLayout(button_frame)
        button_layout.setSpacing(12)

        # Arrange buttons in a 5x3 grid
        for i, (display_name, event_name) in enumerate(buttons_config):
            row = i // 5
            col = i % 5

            button = QPushButton(display_name)
            button.setFont(QFont("Segoe UI", 12, QFont.Weight.DemiBold))
            button.clicked.connect(
                lambda checked, name=event_name, btn=button: self.toggle_event(
                    name, btn
                )
            )

            # Style the button with modern gradient and shadow
            button.setStyleSheet(
                """
                QPushButton {
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                        stop:0 #4a90e2, stop:1 #357abd);
                    color: white;
                    border: none;
                    border-radius: 12px;
                    padding: 18px;
                    text-align: left;
                    font-size: 13px;
                }
                QPushButton:hover {
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                        stop:0 #5ca3f5, stop:1 #4a90e2);
                }
                QPushButton:pressed {
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                        stop:0 #357abd, stop:1 #2868a8);
                }
            """
            )

            self.event_buttons[event_name] = button
            button_layout.addWidget(button, row, col)

        layout.addWidget(button_frame)

    def create_controls(self, layout):
        """Create the notes input and abort button"""
        controls_frame = QFrame()
        controls_frame.setStyleSheet(
            """
            QFrame {
                background: white;
                border-radius: 15px;
                border: 1px solid #dfe4ea;
            }
        """
        )
        controls_layout = QVBoxLayout(controls_frame)
        controls_layout.setSpacing(15)
        controls_layout.setContentsMargins(20, 20, 20, 20)

        # Notes input
        notes_label = QLabel("📝 Optional Notes (only while event active):")
        notes_label.setFont(QFont("Segoe UI", 11, QFont.Weight.DemiBold))
        notes_label.setStyleSheet("QLabel { color: #34495e; }")
        controls_layout.addWidget(notes_label)

        self.notes_input = QLineEdit()
        self.notes_input.setPlaceholderText("Enter optional notes...")
        self.notes_input.setFont(QFont("Segoe UI", 11))
        self.notes_input.setStyleSheet(
            """
            QLineEdit {
                padding: 12px;
                border: 2px solid #e1e8ed;
                border-radius: 8px;
                font-size: 12px;
                background-color: #f8f9fa;
            }
            QLineEdit:focus {
                border-color: #4a90e2;
                background-color: white;
            }
        """
        )
        controls_layout.addWidget(self.notes_input)

        # Buttons layout (horizontal)
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(12)

        # Abort button
        self.abort_button = QPushButton("⚠️ Abort Current Event")
        self.abort_button.setFont(QFont("Segoe UI", 12, QFont.Weight.Bold))
        self.abort_button.clicked.connect(self.abort_event)
        self.abort_button.setStyleSheet(
            """
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #e74c3c, stop:1 #c0392b);
                color: white;
                border: none;
                border-radius: 10px;
                font-size: 13px;
                padding: 15px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #ec7063, stop:1 #e74c3c);
            }
            QPushButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #c0392b, stop:1 #a93226);
            }
        """
        )
        buttons_layout.addWidget(self.abort_button)

        # Missing Events button
        self.missing_event_button = QPushButton("➕ Add Missing Events")
        self.missing_event_button.setFont(QFont("Segoe UI", 12, QFont.Weight.Bold))
        self.missing_event_button.clicked.connect(self.open_missing_event_dialog)
        self.missing_event_button.setStyleSheet(
            """
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #4a90e2, stop:1 #357abd);
                color: white;
                border: none;
                border-radius: 10px;
                font-size: 13px;
                padding: 15px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #5ca3f5, stop:1 #4a90e2);
            }
            QPushButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #357abd, stop:1 #2868a8);
            }
        """
        )
        buttons_layout.addWidget(self.missing_event_button)

        controls_layout.addLayout(buttons_layout)

        layout.addWidget(controls_frame)

        # End Session button at the bottom
        self.end_session_button = QPushButton("🔚 End Session and Close")
        self.end_session_button.setFont(QFont("Segoe UI", 14, QFont.Weight.Bold))
        self.end_session_button.clicked.connect(self.end_session)
        self.end_session_button.setStyleSheet(
            """
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #8e44ad, stop:1 #71368a);
                color: white;
                border: none;
                border-radius: 12px;
                font-size: 15px;
                padding: 18px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #a569bd, stop:1 #8e44ad);
            }
            QPushButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #71368a, stop:1 #5b2c6f);
            }
        """
        )
        layout.addWidget(self.end_session_button)

    def update_status(self, message):
        """Update the status label"""
        self.status_label.setText(message)

    def end_session(self):
        """End the session, record end time, and close the application"""
        # Log session end time
        end_time = datetime.now()
        
        # Calculate duration
        if self.session_start_time:
            duration = end_time - self.session_start_time
            # Format duration as HH:MM:SS
            total_seconds = int(duration.total_seconds())
            hours = total_seconds // 3600
            minutes = (total_seconds % 3600) // 60
            seconds = total_seconds % 60
            duration_str = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
        else:
            duration_str = "N/A"
        
        end_message = f"Session ended at: {end_time.strftime('%Y-%m-%d %H:%M:%S')}"
        
        # If there are active events, ask to abort them
        if self.active_events:
            msg_box = QMessageBox(self)
            msg_box.setIcon(QMessageBox.Icon.Question)
            msg_box.setWindowTitle("Active Event")
            msg_box.setText("There is an active event. Do you want to abort it before ending the session?")
            msg_box.setStandardButtons(
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No | QMessageBox.StandardButton.Cancel
            )
            msg_box.setStyleSheet(
                """
                QMessageBox {
                    background-color: white;
                }
                QMessageBox QLabel {
                    color: #2c3e50;
                    font-size: 12px;
                }
                QPushButton {
                    background-color: #4a90e2;
                    color: white;
                    border: none;
                    border-radius: 6px;
                    padding: 8px 16px;
                    min-width: 80px;
                }
                QPushButton:hover {
                    background-color: #5ca3f5;
                }
            """
            )
            reply = msg_box.exec()
            
            if reply == QMessageBox.StandardButton.Cancel:
                return
            elif reply == QMessageBox.StandardButton.Yes:
                self.abort_event()
        
        # Write end session marker to CSV with start time, end time, and duration
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
                # User skipped session start, so no start time recorded
                writer.writerow([
                    "SESSION END",
                    "N/A",
                    "N/A",
                    end_time.strftime("%Y-%m-%d"),
                    end_time.strftime("%H:%M:%S"),
                    "Session ended, duration: N/A (session start was skipped)"
                ])
        
        print(end_message)
        if self.session_start_time:
            print(f"Total session duration: {duration_str}")
        else:
            print("Session duration: N/A (session start was skipped)")
        
        # Show confirmation and close
        if self.session_start_time:
            message_text = f"{end_message}\nDuration: {duration_str}\n\nThe application will now close."
        else:
            message_text = f"{end_message}\nDuration: N/A (session start was skipped)\n\nThe application will now close."
        
        msg_box = QMessageBox(self)
        msg_box.setIcon(QMessageBox.Icon.Information)
        msg_box.setWindowTitle("Session Ended")
        msg_box.setText(message_text)
        msg_box.setStyleSheet(
            """
            QMessageBox {
                background-color: white;
            }
            QMessageBox QLabel {
                color: #2c3e50;
                font-size: 12px;
            }
            QPushButton {
                background-color: #4a90e2;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 8px 16px;
                min-width: 80px;
            }
            QPushButton:hover {
                background-color: #5ca3f5;
            }
        """
        )
        msg_box.exec()
        
        # Close the application
        self.close()

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
        # Also disable the missing events button
        self.missing_event_button.setEnabled(False)

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
        # Also enable the missing events button
        self.missing_event_button.setEnabled(True)

    def open_missing_event_dialog(self):
        """Open dialog for entering missing events"""
        dialog = QDialog(self)
        dialog.setWindowTitle("⏰ Add Missing Event")
        dialog.setModal(True)
        dialog.setMinimumWidth(500)
        dialog.setStyleSheet(
            """
            QDialog {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #f8f9fa, stop:1 #e9ecef);
            }
        """
        )

        layout = QVBoxLayout(dialog)
        layout.setSpacing(18)
        layout.setContentsMargins(25, 25, 25, 25)

        # Title
        title_label = QLabel("📋 Enter Missing Event Details")
        title_label.setFont(QFont("Segoe UI", 15, QFont.Weight.Bold))
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet(
            """
            QLabel {
                color: #2c3e50;
                padding: 12px;
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #e8f4f8, stop:1 #d5e9f2);
                border-radius: 8px;
            }
            """
        )
        layout.addWidget(title_label)

        # Event selection
        event_label = QLabel("📌 Select Event:")
        event_label.setFont(QFont("Segoe UI", 11, QFont.Weight.DemiBold))
        event_label.setStyleSheet("QLabel { color: #34495e; }")
        layout.addWidget(event_label)

        event_combo = QComboBox()
        event_combo.addItems([
            "🧠 DBS Programming Session",
            "💬 Clinical Interview",
            "🛋️ Lounge Activity",
            "🎉 Surprise",
            "🥽 VR-PAAT",
            "😴 Sleep Period",
            "🍽️ Meal",
            "👥 Social",
            "☕ Break",
            "🔌 IPG Charging",
            "📡 CTM Disconnect",
            "🚶 Walk",
            "🍿 Snack",
            "🧘 Resting state",
            "📝 Other",
        ])
        event_combo.setFont(QFont("Segoe UI", 11))
        event_combo.setStyleSheet(
            """
            QComboBox {
                padding: 10px;
                border: 2px solid #d5dce3;
                border-radius: 8px;
                background-color: white;
                color: #2c3e50;
            }
            QComboBox:focus {
                border-color: #4a90e2;
            }
            QComboBox::drop-down {
                border: none;
            }
            QComboBox QAbstractItemView {
                background-color: white;
                color: #2c3e50;
                selection-background-color: #4a90e2;
                selection-color: white;
            }
        """
        )
        layout.addWidget(event_combo)

        # Start time
        start_label = QLabel("🕐 Start Time:")
        start_label.setFont(QFont("Segoe UI", 11, QFont.Weight.DemiBold))
        start_label.setStyleSheet("QLabel { color: #34495e; }")
        layout.addWidget(start_label)

        start_time_edit = QTimeEdit()
        start_time_edit.setDisplayFormat("HH:mm:ss")
        start_time_edit.setTime(QTime.currentTime())
        start_time_edit.setFont(QFont("Segoe UI", 11))
        start_time_edit.setStyleSheet(
            """
            QTimeEdit {
                padding: 10px;
                border: 2px solid #d5dce3;
                border-radius: 8px;
                background-color: white;
                color: #2c3e50;
            }
            QTimeEdit:focus {
                border-color: #4a90e2;
            }
        """
        )
        layout.addWidget(start_time_edit)

        # End time
        end_label = QLabel("🕑 End Time:")
        end_label.setFont(QFont("Segoe UI", 11, QFont.Weight.DemiBold))
        end_label.setStyleSheet("QLabel { color: #34495e; }")
        layout.addWidget(end_label)

        end_time_edit = QTimeEdit()
        end_time_edit.setDisplayFormat("HH:mm:ss")
        end_time_edit.setTime(QTime.currentTime())
        end_time_edit.setFont(QFont("Segoe UI", 11))
        end_time_edit.setStyleSheet(
            """
            QTimeEdit {
                padding: 10px;
                border: 2px solid #d5dce3;
                border-radius: 8px;
                background-color: white;
                color: #2c3e50;
            }
            QTimeEdit:focus {
                border-color: #4a90e2;
            }
        """
        )
        layout.addWidget(end_time_edit)

        # Optional notes
        notes_label = QLabel("📝 Optional Notes:")
        notes_label.setFont(QFont("Segoe UI", 11, QFont.Weight.DemiBold))
        notes_label.setStyleSheet("QLabel { color: #34495e; }")
        layout.addWidget(notes_label)

        notes_input = QLineEdit()
        notes_input.setPlaceholderText("Enter optional notes...")
        notes_input.setFont(QFont("Segoe UI", 11))
        notes_input.setStyleSheet(
            """
            QLineEdit {
                padding: 10px;
                border: 2px solid #d5dce3;
                border-radius: 8px;
                background-color: white;
                color: #2c3e50;
            }
            QLineEdit:focus {
                border-color: #4a90e2;
            }
        """
        )
        layout.addWidget(notes_input)

        # Buttons
        button_layout = QHBoxLayout()
        button_layout.setSpacing(12)

        submit_button = QPushButton("✅ Submit")
        submit_button.setFont(QFont("Segoe UI", 12, QFont.Weight.Bold))
        submit_button.setStyleSheet(
            """
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #2ecc71, stop:1 #27ae60);
                color: white;
                border: none;
                border-radius: 8px;
                padding: 12px 24px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #58d68d, stop:1 #2ecc71);
            }
            QPushButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #27ae60, stop:1 #229954);
            }
        """
        )
        submit_button.clicked.connect(
            lambda: self.submit_missing_event(
                dialog,
                event_combo.currentText().split(" ", 1)[1] if " " in event_combo.currentText() else event_combo.currentText(),
                start_time_edit.time(),
                end_time_edit.time(),
                notes_input.text(),
            )
        )
        button_layout.addWidget(submit_button)

        cancel_button = QPushButton("❌ Cancel")
        cancel_button.setFont(QFont("Segoe UI", 12, QFont.Weight.Bold))
        cancel_button.setStyleSheet(
            """
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #bdc3c7, stop:1 #95a5a6);
                color: white;
                border: none;
                border-radius: 8px;
                padding: 12px 24px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #d5dbdb, stop:1 #bdc3c7);
            }
            QPushButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #95a5a6, stop:1 #7f8c8d);
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
            msg_box = QMessageBox(dialog)
            msg_box.setIcon(QMessageBox.Icon.Warning)
            msg_box.setWindowTitle("Invalid Time Range")
            msg_box.setText("End time must be after start time.")
            msg_box.setStyleSheet(
                """
                QMessageBox {
                    background-color: white;
                }
                QMessageBox QLabel {
                    color: #2c3e50;
                    font-size: 12px;
                }
                QPushButton {
                    background-color: #e74c3c;
                    color: white;
                    border: none;
                    border-radius: 6px;
                    padding: 8px 16px;
                    min-width: 80px;
                }
                QPushButton:hover {
                    background-color: #ec7063;
                }
            """
            )
            msg_box.exec()
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
        msg_box = QMessageBox(dialog)
        msg_box.setIcon(QMessageBox.Icon.Information)
        msg_box.setWindowTitle("Success")
        msg_box.setText(f"Missing event '{event_name}' has been logged successfully.")
        msg_box.setStyleSheet(
            """
            QMessageBox {
                background-color: white;
            }
            QMessageBox QLabel {
                color: #2c3e50;
                font-size: 12px;
            }
            QPushButton {
                background-color: #2ecc71;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 8px 16px;
                min-width: 80px;
            }
            QPushButton:hover {
                background-color: #58d68d;
            }
        """
        )
        msg_box.exec()

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
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #4a90e2, stop:1 #357abd);
                color: white;
                border: none;
                border-radius: 12px;
                padding: 18px;
                text-align: left;
                font-size: 13px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #5ca3f5, stop:1 #4a90e2);
            }
            QPushButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #357abd, stop:1 #2868a8);
            }
        """
        )

    def set_active_button_style(self, button):
        """Set button to active (teal/green) style"""
        button.setStyleSheet(
            """
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #2ecc71, stop:1 #27ae60) !important;
                color: white !important;
                border: none !important;
                border-radius: 12px !important;
                padding: 18px !important;
                text-align: left !important;
                font-size: 13px !important;
                font-weight: bold !important;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #58d68d, stop:1 #2ecc71) !important;
            }
            QPushButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #27ae60, stop:1 #229954) !important;
            }
        """
        )

    def abort_event(self):
        """Abort the current active event"""
        if not self.active_events:
            msg_box = QMessageBox(self)
            msg_box.setIcon(QMessageBox.Icon.Information)
            msg_box.setWindowTitle("No Active Event")
            msg_box.setText("No active event to abort.")
            msg_box.setStyleSheet(
                """
                QMessageBox {
                    background-color: white;
                }
                QMessageBox QLabel {
                    color: #2c3e50;
                    font-size: 12px;
                }
                QPushButton {
                    background-color: #4a90e2;
                    color: white;
                    border: none;
                    border-radius: 6px;
                    padding: 8px 16px;
                    min-width: 80px;
                }
                QPushButton:hover {
                    background-color: #5ca3f5;
                }
            """
            )
            msg_box.exec()
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
            msg_box = QMessageBox(self)
            msg_box.setIcon(QMessageBox.Icon.Question)
            msg_box.setWindowTitle("Active Event")
            msg_box.setText("There is an active event. Do you want to abort it before closing?")
            msg_box.setStandardButtons(
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No | QMessageBox.StandardButton.Cancel
            )
            msg_box.setStyleSheet(
                """
                QMessageBox {
                    background-color: white;
                }
                QMessageBox QLabel {
                    color: #2c3e50;
                    font-size: 12px;
                }
                QPushButton {
                    background-color: #4a90e2;
                    color: white;
                    border: none;
                    border-radius: 6px;
                    padding: 8px 16px;
                    min-width: 80px;
                }
                QPushButton:hover {
                    background-color: #5ca3f5;
                }
            """
            )
            reply = msg_box.exec()

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

    # Show startup dialog
    startup_dialog = StartupDialog()
    if startup_dialog.exec() != QDialog.DialogCode.Accepted:
        # User closed the dialog without choosing, exit app
        sys.exit(0)

    # Get whether to record session start
    record_start = startup_dialog.record_start

    # Create and show the main window
    window = EventLogger(project_id, record_start)
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
