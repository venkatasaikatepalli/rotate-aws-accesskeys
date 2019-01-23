import logging
from flask import Flask, render_template
from scripts.iam import IAMManager

__author__ = "Venkata.Sai.Kateppalli<venkatasaikatepalli@gmail.com>"
__version__ = "1.0"

app = Flask(__name__)

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/rotate-keys/")
def rotate_keys():
    return render_template('index.html')

@app.route("/rotate/")
def rotate():
    ref = IAMManager()
    return ref.rotate_user_keys()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)
