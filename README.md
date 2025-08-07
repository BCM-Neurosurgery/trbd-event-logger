# TRBD Event Logger

A cross-platform desktop ap## Requirements

- Python 3.7+
- PyQt6

## Distribution

### Ubuntu Package (.deb)
```bash
chmod +x build_deb.sh
./build_deb.sh
sudo dpkg -i trbd-event-logger_1.0.deb
```

### Standalone Executable
```bash
pip install pyinstaller
pyinstaller --onefile --windowed event_logger_qt.py
# Executable in dist/event_logger_qt
```

### Simple Distribution
```bash
chmod +x create_tarball.sh
./create_tarball.sh
# Creates trbd-event-logger-1.0.tar.gz
```

## Authorion for logging clinical events during TRBD Clinical Trial interactions at Baylor College of Medicine.

## Features

- **10 Event Types**: DBS Programming Session, Clinical Interview, Lounge Activity, Surprise, VR-PAAT, Sleep Period, Meal, Social, Break, Other
- **Real-time Logging**: Start/stop events with instant audio feedback
- **CSV Export**: Automatic logging to timestamped CSV files
- **Notes Support**: Optional notes for each event
- **Abort Functionality**: Safely abort events if needed
- **Cross-platform**: Works on Windows, macOS, and Linux

## Installation

1. Install Python 3.7+ and PyQt6:
   ```bash
   pip install PyQt6
   ```

2. Clone or download this repository

## Usage

### Basic Usage
```bash
python event_logger_qt.py
```

### With Project ID
```bash
python event_logger_qt.py TRBD001
```

## How It Works

1. **Start Event**: Click any event button - it turns green and begins timing
2. **End Event**: Click the same button again to stop and log the event
3. **Switch Events**: Click a different button to end current and start new event
4. **Add Notes**: Type in the notes field while an event is active
5. **Abort**: Use "Abort Current Event" button to cancel without completion

## Output

Events are logged to CSV files with format: `event_log_MMDD_HH_MM.csv` or `{PROJECT_ID}_event_log_MMDD_HH_MM.csv`

Columns: Event, Start Date, Start Time, End Date, End Time, Notes

## Requirements

- Python 3.12
- PyQt6

## Author

Baylor College of Medicine - TRBD Clinical Trial Team