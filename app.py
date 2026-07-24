from flask import Flask, render_template, request, redirect, url_for, session
from questions import questions

app = Flask(__name__)
app.secret_key = "gk_master_secret_key"


@app.route("/")
def home():
    session.clear()
    return render_template("index.html")


@app.route("/quiz")
def quiz():

    current = int(request.args.get("q", 0))

    if current >= len(questions):
        return redirect(url_for("result"))

    question = questions[current]

    return render_template(
        "quiz.html",
        question=question,
        current=current,
        total=len(questions)
    )
@app.route("/answer", methods=["POST"])
def answer():

    current = int(request.form["current"])
    selected = request.form["answer"]

    if "score" not in session:
        session["score"] = 0

    if "results" not in session:
        session["results"] = []

    correct = questions[current]["answer"]

    is_correct = selected == correct

    if is_correct:
        session["score"] += 1

    session["results"].append({
        "question": questions[current]["question"],
        "user": selected,
        "correct": correct,
        "is_correct": is_correct
    })

    return redirect(url_for("quiz", q=current + 1))


@app.route("/result")
def result():

    score = session.get("score", 0)
    results = session.get("results", [])

    return render_template(
        "result.html",
        score=score,
        total=len(questions),
        results=results
    )


if __name__ == "__main__":
    app.run(debug=True)

