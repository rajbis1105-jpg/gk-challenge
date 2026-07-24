from flask import Flask, render_template, request, redirect, url_for, session
from questions import questions

app = Flask(__name__)

app.secret_key = "gk_master_secret_key"


# Home Page
@app.route("/")
def home():
    session.clear()
    return render_template("index.html")


# Start Quiz
@app.route("/quiz")
def quiz():

    current = int(request.args.get("q", 0))

    # সব প্রশ্ন শেষ হলে result page
    if current >= len(questions):
        return redirect(url_for("result"))

    question = questions[current]

    return render_template(
        "quiz.html",
        question=question,
        current=current,
        total=len(questions)
    )


# Answer Check
@app.route("/answer", methods=["POST"])
def answer():

    current = int(request.form.get("current"))
    selected = request.form.get("answer")


    # প্রথমবার session তৈরি
    if "score" not in session:
        session["score"] = 0

    if "results" not in session:
        session["results"] = []


    correct_answer = questions[current]["answer"]

    is_correct = selected == correct_answer


    # Score update
    if is_correct:
        session["score"] = session["score"] + 1


    # Result save
    results = session["results"]

    results.append({

        "number": current + 1,

        "question": questions[current]["question"],

        "selected": selected,

        "correct": correct_answer,

        "is_correct": is_correct

    })


    session["results"] = results


    # Next question
    return redirect(
        url_for(
            "quiz",
            q=current + 1
        )
    )



# Result Page
@app.route("/result")
def result():

    total = len(questions)

    score = session.get("score", 0)

    results = session.get("results", [])


    wrong = total - score


    percentage = 0

    if total > 0:
        percentage = round(
            (score / total) * 100,
            2
        )


    wrong_questions = []

    for item in results:

        if not item["is_correct"]:

            wrong_questions.append(item)



    return render_template(

        "result.html",

        score=score,

        total=total,

        wrong=wrong,

        percentage=percentage,

        results=results,

        wrong_questions=wrong_questions

    )



if __name__ == "__main__":
    app.run(debug=True)