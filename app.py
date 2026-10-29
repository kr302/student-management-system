from flask import Flask, render_template, request, redirect, url_for
import json
from pathlib import Path

app = Flask(__name__)
DATA_FILE = Path(__file__).parent / "students_data.json"


def load_students():
    if DATA_FILE.exists():
        with open(DATA_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    return {}


def save_students(students):
    with open(DATA_FILE, "w", encoding="utf-8") as file:
        json.dump(students, file, indent=4)


@app.route("/")
def home():
    students = load_students()
    query = request.args.get("q", "").strip().lower()

    records = list(students.values())
    if query:
        records = [
            s for s in records
            if query in str(s.get("roll_no", "")).lower()
            or query in s.get("name", "").lower()
        ]

    total = len(students)
    low = sum(
        float(s.get("attendance_pct", 0)) < 75
        for s in students.values()
    )
    average = (
        sum(float(s.get("attendance_pct", 0))
            for s in students.values()) / total
        if total else 0
    )

    return render_template(
        "index.html",
        students=records,
        total=total,
        low=low,
        average=average,
        query=query
    )


@app.route("/add", methods=["POST"])
def add_student():
    students = load_students()
    roll = request.form.get("roll_no", "").strip()
    name = request.form.get("name", "").strip()
    branch = request.form.get("branch", "").strip()

    try:
        attendance = float(request.form.get("attendance", ""))
    except ValueError:
        return "Please enter a valid attendance percentage.", 400

    if not roll or not name or not branch or not 0 <= attendance <= 100:
        return "Please enter valid student details.", 400

    if roll in students:
        return "This roll number already exists.", 400

    students[roll] = {
        "roll_no": roll,
        "name": name,
        "branch": branch,
        "attendance_pct": attendance
    }
    save_students(students)
    return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(debug=True)