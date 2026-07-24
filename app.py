from flask import Flask, render_template, request
from questions import questions

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/quiz", methods=["GET", "POST"])
def quiz():

    if request.method == "POST":

        score = 0
        results = []

        for i, q in enumerate(questions):

            user_answer = request.form.get(f"q{i}")
            correct_answer = q["answer"]

            is_correct = user_answer == correct_answer

            if is_correct:
                score += 1

            results.append({
                "question": q["question"],
                "options": q["options"],
                "user_answer": user_answer if user_answer else "No Answer",
                "correct_answer": correct_answer,
                "is_correct": is_correct
            })

        return render_template(
            "result.html",
            score=score,
            total_questions=len(questions),
            results=results
        )

    return render_template(
        "quiz.html",
        questions=questions
    )


if __name__ == "__main__":
    app.run(debug=True)