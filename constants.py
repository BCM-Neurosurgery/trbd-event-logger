"""
Constants for TRBD Event Logger
Contains event names, button configurations, and other constant values
"""

# Event button configurations with emojis and full names
EVENT_BUTTONS = [
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
    ("Clinical Scales", "Clinical Scales"),
    ("📝 Other", "Other"),
]

# Event names for missing event dialog (with emojis)
MISSING_EVENT_OPTIONS = [
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
    "Clinical Scales",
    "📝 Other",
]

# CSV header columns
CSV_HEADERS = ["Event", "Start Date", "Start Time", "End Date", "End Time", "Notes"]

# Window dimensions
MAIN_WINDOW_SIZE = (1000, 700)
STARTUP_DIALOG_SIZE = (600, 350)
MISSING_EVENT_DIALOG_SIZE = (500, 400)

# Grid layout configuration
BUTTON_GRID_COLUMNS = 5
BUTTON_GRID_SPACING = 12

# Font configuration
DEFAULT_FONT_FAMILY = "Segoe UI"
