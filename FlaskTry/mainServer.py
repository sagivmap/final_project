from flask import Flask, render_template, request, flash, redirect
from Crawler import FBCrawler
import os
app = Flask(__name__)

UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uploads')

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def main():
    return render_template('index.html')

def crawl_facebook():
    email = request.form['emailForFacebook']
    password = request.form['passwordForFacebook']
    print(email, password)
    return render_template('index.html')

def upload_file():
    # check if the post request has the file part
    if 'file' not in request.files:
        return redirect(request.url)
    file = request.files['file']
    if file:
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
        return render_template('index.html')

@app.route('/', methods=['POST'])
def handle_posts():
    if request.method == 'POST':
        if request.form["button"]=="Crawl":
            return crawl_facebook()

        elif request.form["button"]=="Upload":
            return upload_file()

        elif request.form["button"]=="MoveToManuallyAddPage":
            return render_template('addManuallyPage.html')


if __name__ == '__main__':
    app.config['DEBUG'] = True
    app.run()