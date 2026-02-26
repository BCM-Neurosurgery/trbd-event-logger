"""
Utility functions for TRBD Event Logger
Helper functions for duration calculation, message boxes, and logging
"""

import csv
from datetime import datetime
from PyQt6.QtWidgets import QMessageBox

from styles import MESSAGE_BOX_INFO_STYLE, MESSAGE_BOX_WARNING_STYLE, MESSAGE_BOX_QUESTION_STYLE


def calculate_duration(start_time, end_time):
    """
    Calculate duration between two datetime objects
    
    Args:
        start_time: datetime object for start time
        end_time: datetime object for end time
    
    Returns:
        str: Duration formatted as HH:MM:SS
    """
    if not start_time or not end_time:
        return "N/A"
    
    duration = end_time - start_time
    total_seconds = int(duration.total_seconds())
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    seconds = total_seconds % 60
    
    return f"{hours:02d}:{minutes:02d}:{seconds:02d}"


def log_to_csv(csv_file, event_name, start_time, end_time, notes=""):
    """
    Log an event to the CSV file
    
    Args:
        csv_file: Path to the CSV file
        event_name: Name of the event
        start_time: datetime object for start time
        end_time: datetime object for end time (can be None)
        notes: Optional notes for the event
    """
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

    with open(csv_file, "a", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(data)

    print(f"Logged event:")
    print(f"  Event: {event_name}")
    print(f"  Start: {start_time}")
    print(f"  End: {end_time}")
    print(f"  Notes: {notes}")


def create_message_box(parent, icon, title, text, style=None):
    """
    Create a styled message box
    
    Args:
        parent: Parent widget
        icon: QMessageBox.Icon enum value
        title: Window title
        text: Message text
        style: Optional custom stylesheet (defaults to INFO_STYLE)
    
    Returns:
        QMessageBox: Configured message box
    """
    msg_box = QMessageBox(parent)
    msg_box.setIcon(icon)
    msg_box.setWindowTitle(title)
    msg_box.setText(text)
    
    if style is None:
        style = MESSAGE_BOX_INFO_STYLE
    
    msg_box.setStyleSheet(style)
    return msg_box


def show_info_message(parent, title, text):
    """Show an information message box"""
    msg_box = create_message_box(parent, QMessageBox.Icon.Information, title, text, MESSAGE_BOX_INFO_STYLE)
    return msg_box.exec()


def show_warning_message(parent, title, text):
    """Show a warning message box"""
    msg_box = create_message_box(parent, QMessageBox.Icon.Warning, title, text, MESSAGE_BOX_WARNING_STYLE)
    return msg_box.exec()


def show_question_message(parent, title, text, buttons=None):
    """Show a question message box with custom buttons"""
    msg_box = create_message_box(parent, QMessageBox.Icon.Question, title, text, MESSAGE_BOX_QUESTION_STYLE)
    
    if buttons:
        msg_box.setStandardButtons(buttons)
    else:
        msg_box.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
    
    return msg_box.exec()


def get_current_date_folder():
    """
    Get the current date folder name in YYYY-MM-DD format
    
    Returns:
        str: Date folder name (e.g., "2025-01-15")
    """
    return datetime.now().strftime("%Y-%m-%d")


def get_current_timestamp_filename():
    """
    Get a timestamp-based filename for event logs
    
    Returns:
        str: Filename in format "event_log_MMDD_HH_MM_SS.csv"
    """
    return datetime.now().strftime("event_log_%m%d_%H_%M_%S.csv")


def format_datetime_for_display(dt):
    """
    Format datetime for user-friendly display
    
    Args:
        dt: datetime object
    
    Returns:
        str: Formatted datetime string
    """
    if not dt:
        return "N/A"
    return dt.strftime("%Y-%m-%d %H:%M:%S")


def parse_event_name(event_display_text):
    """
    Extract the actual event name from display text with emoji
    
    Args:
        event_display_text: Text with emoji prefix (e.g., "🧠 DBS Programming Session")
    
    Returns:
        str: Event name without emoji (e.g., "DBS Programming Session")
    """
    if " " in event_display_text:
        return event_display_text.split(" ", 1)[1]
    return event_display_text
