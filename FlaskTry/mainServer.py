from flask import Flask, render_template, request
from Crawler import FBCrawler
app = Flask(__name__)

@app.route('/')
def main():
    return render_template('index.html')

@app.route('/', methods=['GET', 'POST'])
def foo():
    email = request.form['aaaaa']
    print (email)
    return render_template('index.html')

@app.route('/index2')
def index2():
    return render_template('index2.html')


if __name__ == '__main__':
    app.run()