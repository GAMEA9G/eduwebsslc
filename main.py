from flask import Flask, render_template, request
import random
import json
import logging

# Configure logging
logging.basicConfig(filename='app.log', level=logging.ERROR)
correct_answer ={}
random_question ={}
question1 ={}
app = Flask(__name__)

def load_subjects():
    with open('subjects.json', 'r') as file:
        return json.load(file)

subjects = load_subjects()['subjects']

@app.route('/')
def home():
    return render_template('home.html', subjects=subjects)

@app.route('/<subject>/<chapter>/')
def index(subject, chapter):
    if subject not in subjects or chapter not in subjects[subject]:
        return "Invalid subject or chapter"
    
    questions = subjects[subject][chapter]
    if not questions:
        return "No questions available for this subject and chapter"
    
    random_question = random.choice(questions)
    return render_template('index.html', question=random_question, subject=subject, chapter=chapter, correctAnswer=random_question['answer'])

@app.route('/<subject>/<chapter>/submit', methods=['POST'])
def submit(subject, chapter):
    if request.method == 'POST':
        user_answer = request.form.get('answerInput')
        question = request.form.get('question', ' ')

        # Retrieve the correct answer from the question dictionary
        correct_answer = request.form.get('correctAnswer', '')

        return render_template('index.html', userAnswer=user_answer, correctAnswer=correct_answer, subject=subject, chapter=chapter, question=question)


if __name__ == '__main__':
    app.run(debug=False)
