from flask import Flask, render_template, request, redirect, url_for, jsonify
import json

app = Flask(__name__)

# Load questions from JSON
def load_questions():
    with open('questions.json', 'r') as file:
        data = json.load(file)
    return data['questions']

# Route to display the quiz questions
@app.route('/')
def index():
    questions = load_questions()
    return render_template('index.html', questions=questions)

# Route to handle form submission and calculate results
@app.route('/submit', methods=['POST'])
def submit():
    questions = load_questions()
    user_answers = request.form

    # Calculate the score
    correct_count = 0
    results = []
    for question in questions:
        qid = str(question['id'])
        correct = False
        if question['type'] == 'single':
            # Check if the single answer is correct and exists in user responses
            user_answer = user_answers.get(qid)
            if user_answer and user_answer == question['correct_answer']:
                correct = True
        elif question['type'] == 'multiple':
            # Check if all selected answers match the correct answers for multiple-choice questions
            selected_answers = user_answers.getlist(qid)
            if selected_answers and set(selected_answers) == set(question['correct_answers']):
                correct = True

        # Track results for each question
        results.append({
            'question': question['question'],
            'correct': correct,
            'user_answer': user_answers.getlist(qid),
            'correct_answer': question.get('correct_answers') if question['type'] == 'multiple' else question['correct_answer']
        })

        if correct:
            correct_count += 1

    # Calculate percentage
    score_percentage = round((correct_count / len(questions)) * 100)


    # Render result page
    return render_template('result.html', results=results, score=score_percentage)

if __name__ == '__main__':
    app.run(debug=True)
