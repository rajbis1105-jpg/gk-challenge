from flask import Flask, render_template, request
from questions import questions

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/quiz", methods=["GET", "POST"])
def quiz():
    if request.method == "POST":
        score = 0

        for i, q in enumerate(questions):
            user_answer = request.form.get(f"q{i}")

            if user_answer == q["answer"]:
                score += 1

        return render_template(
            "result.html",
            score=score,
            total_questions=len(questions)
        )

    return render_template(
        "quiz.html",
        questions=questions
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)