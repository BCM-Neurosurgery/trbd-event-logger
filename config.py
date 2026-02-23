from pathlib import Path

VALID_IDS = ['AA', 'TRBD', 'P']
STUDY_IDS = {'AA': 'AA-56119', 'TRBD': 'TRBD-53761', 'P': 'PerceptOCD-48392'}
ROOT = Path('C:/NBU_Data/Logger')
EVENTS = [
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

SOURCE_PARSER = r"C:\Users\kasra\OneDrive\Desktop\logger.bat"