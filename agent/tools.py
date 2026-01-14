import csv
from datetime import datetime

FILE = "leads.csv"

def lead_capture_tool(data):

    with open(FILE, "a", newline="") as f:
        writer = csv.writer(f)

        writer.writerow([
            data["name"],
            data["email"],
            data["company"],
            datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ])

    return "✅ Lead captured successfully! Our team will contact you soon."
