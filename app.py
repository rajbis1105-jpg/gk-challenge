from flask import Flask, render_template, request
from questions import questions

@app.route("/quiz", methods=["GET", "POST"])
def quiz():

    page = int(request.args.get("page", 1))

    start = (page - 1) * 10
    end = start + 10

    current_questions = questions[start:end]

    if request.method == "POST":

        score = 0
        results = []

        for i, q in enumerate(questions):
            user_answer = request.form.get(f"q{i}")

            is_correct = user_answer == q["answer"]

            if is_correct:
                score += 1

            results.append({
                "question": q["question"],
                "user_answer": user_answer if user_answer else "No Answer",
                "correct_answer": q["answer"],
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
        questions=current_questions,
        page=page,
        total_pages=(len(questions) + 9) // 10
    )