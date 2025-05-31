from flask import Flask, render_template, request, redirect, session, url_for
from db import users_collection, chat_collection
from chatbot import ask_math_bot
import bcrypt

app = Flask(__name__)
app.secret_key = "your_secret_key"

@app.route('/')
def home():
    return redirect('/login')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        existing_user = users_collection.find_one({'username': request.form['username']})
        if existing_user:
            return "User already exists"
        user = {
            "username": request.form['username'],
            "password": bcrypt.hashpw(request.form['password'].encode('utf-8'), bcrypt.gensalt())
        }
        users_collection.insert_one(user)
        return redirect('/login')
    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = users_collection.find_one({"username": request.form['username']})
        if user and bcrypt.checkpw(request.form['password'].encode('utf-8'), user['password']):
            session['username'] = user['username']
            return redirect('/chat')
    return render_template('login.html')

@app.route('/chat', methods=['GET', 'POST'])
def chat():
    if 'username' not in session:
        return redirect('/login')

    response = ""
    history = list(chat_collection.find({"username": session['username']}))

    if request.method == 'POST':
        user_input = request.form['question']
        response = ask_math_bot(user_input)
        chat_collection.insert_one({
            "username": session['username'],
            "question": user_input,
            "response": response
        })
        history.append({"question": user_input, "response": response})

    return render_template('index.html', response=response, history=history)

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')

if __name__ == '__main__':
    app.run(debug=True)
