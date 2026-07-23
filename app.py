from flask import Flask, render_template, request
from questions import questions

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/quiz", methods=["GET", "POST"])
def quiz():

    page = int(request.args.get("page", 1))

    start = (page - 1) * 10
    end = start + 10

    current_questions = questions[start:end]


    if request.method == "POST":

        score = 0

        for i, q in enumerate(questions):

            user_answer = request.form.get(f"q{i}")

            if user_answer == q["answer"]:
                score += 1


        return render_template("result.html", score=score)


    return render_template(
        "quiz.html",
        questions=current_questions,
        page=page,
        total_pages=(len(questions) + 9) // 10
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)