"""
Configuration settings for different deployment environments
Supports Jamail and NBU laptop configurations
"""

from pathlib import Path

# Configuration profiles
CONFIGS = {
    "Jamail": {
        "app_name": "Jamail Event Logger",
        "root_path": Path("C:/Users/prove/Desktop/Notes/"),
        "record_start_time": True,
        "run_parser": False,
        "parser_path": None,
        "events": [
            ("🧠 DBS Programming", "DBS Programming Session"),
            ("💬 Clinical Interview", "Clinical Interview"),
            ("🎯 PRT", "PRT"),
            ("⚡ ERP", "ERP"),
            ("🥽 PAAT", "PAAT"),
            ("🧘 Resting", "Resting"),
            ("📝 Other", "Other"),
        ],
        "valid_ids": ['AA', 'TRBD', 'P'],
        "study_ids": {
            'AA': 'AA-56119',
            'TRBD': 'TRBD-53761',
            'P': 'PerceptOCD-48392'
        }
    },
    "NBU": {
        "app_name": "TRBD Event Logger",
        "root_path": Path("C:/NBU_Data/Logger"),
        "record_start_time": False,
        "run_parser": False,
        "parser_path": None,
        "events": [
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
        ],
        "valid_ids": ['AA', 'TRBD', 'P'],
        "study_ids": {
            'AA': 'AA-56119',
            'TRBD': 'TRBD-53761',
            'P': 'PerceptOCD-48392'
        }
    }
}


class AppConfig:
    """Application configuration manager"""
    
    def __init__(self, config_name="NBU"):
        """Initialize with a configuration profile"""
        if config_name not in CONFIGS:
            raise ValueError(f"Unknown configuration: {config_name}. Available: {list(CONFIGS.keys())}")
        
        self.config_name = config_name
        self._config = CONFIGS[config_name]
    
    @property
    def app_name(self):
        """Application name"""
        return self._config["app_name"]
    
    @property
    def root_path(self):
        """Root directory path"""
        return self._config["root_path"]
    
    @property
    def record_start_time(self):
        """Whether to record session start time by default"""
        return self._config["record_start_time"]
    
    @property
    def run_parser(self):
        """Whether to run source parser after session"""
        return self._config["run_parser"]
    
    @property
    def parser_path(self):
        """Path to parser batch file"""
        return self._config["parser_path"]
    
    @property
    def events(self):
        """List of event buttons (display_name, event_name)"""
        return self._config["events"]
    
    @property
    def event_names(self):
        """List of event names only"""
        return [name for _, name in self._config["events"]]
    
    @property
    def event_display_names(self):
        """List of display names with emojis"""
        return [display for display, _ in self._config["events"]]
    
    @property
    def valid_ids(self):
        """Valid patient ID prefixes"""
        return self._config["valid_ids"]
    
    @property
    def study_ids(self):
        """Mapping of ID prefixes to study IDs"""
        return self._config["study_ids"]
    
    def get_study_id(self, patient_id):
        """Get study ID from patient ID prefix"""
        for prefix in self.valid_ids:
            if patient_id.upper().startswith(prefix):
                return self.study_ids[prefix]
        return "Unknown-Study"


# Default configuration
DEFAULT_CONFIG = "NBU"
