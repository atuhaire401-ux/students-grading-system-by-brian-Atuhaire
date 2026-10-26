
from flask import Flask, request, render_template_string

app = Flask(__name__)

SUBJECTS = [
    "Mathematics", "English", "Computer", "Economics",
    "Physics", "Geography", "CRE"
]

PAGE = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Student Grading System</title>
<style>
* { box-sizing: border-box; }
body {
    margin: 0;
    padding: 20px;
    font-family: Arial, sans-serif;
    background: #eef3f8;
    color: #172b4d;
}
.container {
    max-width: 600px;
    margin: auto;
    background: white;
    padding: 24px;
    border-radius: 16px;
    box-shadow: 0 5px 20px #0001;
}
h1 { text-align: center; color: #0756a5; }
.subtitle { text-align: center; color: #64748b; }
label {
    display: block;
    margin-top: 14px;
    font-weight: bold;
}
input {
    width: 100%;
    padding: 12px;
    margin-top: 6px;
    border: 1px solid #cbd5e1;
    border-radius: 8px;
    font-size: 16px;
}
button {
    width: 100%;
    padding: 14px;
    margin-top: 22px;
    border: none;
    border-radius: 8px;
    background: #0756a5;
    color: white;
    font-size: 17px;
    font-weight: bold;
    cursor: pointer;
}
button:hover { background: #043e7b; }
.results {
    margin-top: 24px;
    padding: 18px;
    border-radius: 10px;
    background: #eaf5ff;
    overflow-wrap: anywhere;
}
.results p { margin: 12px 0; }
.error {
    color: #b91c1c;
    background: #fee2e2;
    padding: 12px;
    border-radius: 8px;
}
footer {
    margin-top: 24px;
    text-align: center;
    color: #64748b;
    font-size: 13px;
}
</style>
</head>
<body>
<div class="container">
    <h1>Student Grading System</h1>
    <p class="subtitle">Enter marks for all seven subjects</p>

    {% if error %}
        <p class="error">{{ error }}</p>
    {% endif %}

    <form method="POST">
        <label>Student Name</label>
        <input name="student_name" required
               value="{{ name }}" placeholder="Enter full name">

        {% for subject in subjects %}
        <label>{{ subject }} (out of 100)</label>
        <input type="number" name="{{ subject }}"
               min="0" max="100" step="any" required
               value="{{ marks.get(subject, '') }}"
               placeholder="Enter marks">
        {% endfor %}

        <button type="submit">Calculate Results</button>
    </form>

    {% if result %}
    <div class="results">
        <h2>Student Results</h2>
        <p><b>Name:</b> {{ result.name }}</p>
        <p><b>Total:</b> {{ result.total }} / 700</p>
        <p><b>Average:</b> {{ "%.2f"|format(result.average) }}%</p>
        <p><b>Grade:</b> {{ result.grade }}</p>
        <p><b>Comment:</b> {{ result.comment }}</p>
    </div>
    {% endif %}

    <footer>Student Grading System | ICT Project</footer>
</div>
</body>
</html>
"""


@app.route("/", methods=["GET", "POST"])
def home():
    result = None
    error = None
    name = ""
    marks = {}

    if request.method == "POST":
        name = request.form.get("student_name", "").strip()

        try:
            if not name:
                raise ValueError("Please enter the student's name.")

            for subject in SUBJECTS:
                value = request.form.get(subject, "").strip()

                if not value:
                    raise ValueError(
                        "Please enter marks for " + subject + "."
                    )

                mark = float(value)

                if not 0 <= mark <= 100:
                    raise ValueError(
                        subject + " marks must be between 0 and 100."
                    )

                marks[subject] = mark

            total = sum(marks.values())
            average = total / len(SUBJECTS)

            if average >= 80:
                grade, comment = "A", "EXCELLENT"
            elif average >= 70:
                grade, comment = "B", "VERY GOOD"
            elif average >= 60:
                grade, comment = "C", "GOOD"
            elif average >= 50:
                grade, comment = "D", "FAIR"
            else:
                grade, comment = "F", "FAILED"

            result = {
                "name": name,
                "total": total,
                "average": average,
                "grade": grade,
                "comment": comment
            }

        except ValueError as exc:
            error = str(exc)

    return render_template_string(
        PAGE,
        subjects=SUBJECTS,
        result=result,
        error=error,
        name=name,
        marks=marks
    )


if __name__ == "__main__":
    import os
    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 5000)),
        debug=False
    )
