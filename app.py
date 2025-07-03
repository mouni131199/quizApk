from flask import Flask, render_template, request, redirect, session
from flask_pymongo import PyMongo
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'supersecretkey'
app.config['MONGO_URI'] = 'mongodb+srv://mounirongali99:z7eevIOrku7rN08o@cluster0.jvlw0p5.mongodb.net/quizdb?retryWrites=true&w=majority&appName=Cluster0'

mongo = PyMongo(app)
questions_col = mongo.db.questions
results_col = mongo.db.results

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session['name'] = request.form['name']
        session['email'] = request.form['email']
        return redirect('/quiz')
    return render_template('login.html')

@app.route('/quiz', methods=['GET', 'POST'])
def quiz():
    email = session.get('email')
    name = session.get('name')

    if not email or not name:
        return redirect('/')  # Redirect to login if session data is missing

    previous_attempt = results_col.find_one({'email': email})
    
    if previous_attempt:
        score = previous_attempt.get('score', 0)
        total = previous_attempt.get('total', 0)
        return render_template('result.html', score=score, total=total)

    questions = list(questions_col.find({}, {'_id': 0}))

    if request.method == 'POST':
        score = 0
        for i, q in enumerate(questions):
            user_answer = request.form.get(f'q{i}')
            if user_answer == q['answer']:
                score += 1
        results_col.insert_one({
            'name': name,
            'email': email,
            'score': score,
            'total': len(questions),
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        })
        return render_template('result.html', score=score, total=len(questions))
    
    return render_template('quiz.html', questions=questions)

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
