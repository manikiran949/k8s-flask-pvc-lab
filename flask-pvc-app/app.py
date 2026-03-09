from flask import Flask
import os
from datetime import datetime

app = Flask(__name__)
DATA_FILE = "/data/visits.txt"

@app.route("/")
def hello():
    # Ensure directory exists
    os.makedirs("/data", exist_ok=True)
    
    # Write current time to the file
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(DATA_FILE, "a") as f:
        f.write(f"Visited at: {now}\n")
    
    # Read all visits to display on the webpage
    with open(DATA_FILE, "r") as f:
        visits = f.read()
        
    return f"<h1>Flask App Persistence Test</h1><p>Below is the data read from the PVC (/data/visits.txt):</p><pre>{visits}</pre>"

if __name__ == "__main__":
    # Listen on all network interfaces
    app.run(host="0.0.0.0", port=5000)