from flask import Flask
from flask import render_template

app = Flask(__name__)

@app.route('/templates/index.html')
def main():
    return render_template('index.html')

@app.route('/templates/about.html')
def about():
    return render_template('about.html')

@app.route('/templates/signin.html')
def signin():
    return render_template('signin.html')

@app.route('/templates/signup.html')
def signup():
    return render_template('signup.html')

if __name__ == "__main__":
    app.run()