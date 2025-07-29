"""
Flask app to log clinical events of interest for
TRBD Clinical Trial with Baylor College of Medicine.
Code is only to be used by medical students logging events
with patient during interactions.

Code is not meant to be modified, altered, or copied
for any other purpose besides TRBD Clinical trial.

@author  Isha Chakraborty; Yewen
@version 1.3 04/07/2025
"""

import sys
from flask import Flask, render_template, request, jsonify
from datetime import datetime
import pandas as pd
import os

project_id = ""
if len(sys.argv) >= 2:
    project_id = sys.argv[1]

app = Flask(__name__)

time_stamp = datetime.now().strftime("%m%d_%H_%M")
output_folder = ""
if project_id == "":
    data_file = os.path.join(output_folder, f"event_log_{time_stamp}.csv")
else:
    data_file = os.path.join(output_folder, f"{project_id}_event_log_{time_stamp}.csv")

if not os.path.exists(data_file):
    df = pd.DataFrame(
        columns=["Event", "Start Date", "Start Time", "End Date", "End Time", "Notes"]
    )
    df.to_csv(data_file, index=False, mode="w", header=True)

active_events = {}


def log_event(event_name, start_time, end_time, notes=""):
    end_date = end_time.strftime("%Y-%m-%d") if end_time else "N/A"
    end_time_str = end_time.strftime("%H:%M:%S") if end_time else "N/A"

    data = {
        "Event": event_name,
        "Start Date": start_time.strftime("%Y-%m-%d"),
        "Start Time": start_time.strftime("%H:%M:%S"),
        "End Date": end_date,
        "End Time": end_time_str,
        "Notes": notes,
    }
    df = pd.DataFrame([data])
    df.to_csv(data_file, mode="a", header=False, index=False)
    print(f"Logged event to {os.path.abspath(data_file)}:")
    print(data)


@app.route("/toggle_event", methods=["POST"])
def toggle_event():
    data = request.get_json()
    event_name = data["event"]
    notes = data.get("notes", "")

    if event_name in active_events:
        start_time = active_events.pop(event_name)
        log_event(event_name, start_time, datetime.now(), notes)
        return jsonify(
            {
                "message": f"Ended {event_name}",
                "status": "Press a button to start an event",
                "active_event": None,
            }
        )
    else:
        active_events.clear()
        active_events[event_name] = datetime.now()
        return jsonify(
            {
                "message": f"Started {event_name}",
                "status": f"{event_name} has started",
                "active_event": event_name,
            }
        )


@app.route("/abort_event", methods=["POST"])
def abort_event():
    data = request.get_json()
    notes = data.get("notes", "")
    event_name = next(iter(active_events), None)

    if event_name:
        start_time = active_events.pop(event_name)
        notes = f"ABORTED: {notes}" if notes else "ABORTED"
        log_event(event_name, start_time, None, notes)
        return jsonify(
            {
                "message": f"Aborted {event_name}",
                "status": "Event Aborted",
                "active_event": None,
            }
        )
    else:
        return jsonify(
            {
                "message": "No active event to abort.",
                "status": "No active event",
                "active_event": None,
            }
        )


@app.route("/")
def home():
    return render_template("index.html", project_id=project_id)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5001)
