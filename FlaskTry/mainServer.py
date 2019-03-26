from flask import Flask, render_template, request, redirect

import os
import json
app = Flask(__name__)

UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uploads')
PATH_TO_JSON = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static','graphFile.json')

ID_FOR_NODE = 1

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['PATH_TO_JSON'] = PATH_TO_JSON
app.config['ID_FOR_NODE'] = 1
@app.route('/')
def main():
    return render_template('index.html')

def crawl_facebook():
    email = request.form['emailForFacebook']
    password = request.form['passwordForFacebook']
    print(email, password)
    return render_template('index.html')

def crawl_twitter():
    nick_name = request.form['twitterName']
    print(nick_name)
    return render_template('index.html')

def upload_file():
    # check if the post request has the file part
    if 'file' not in request.files:
        return redirect(request.url)
    file = request.files['file']
    if file:
        path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(path)
        import csv
        import json
        # csv to Json
        csvfile = open(path, mode='r')
        jsonfile = open('file.json', 'w')
        fieldnames = ("ID","Name","TF","MF","AUA","FD","CF")
        reader = csv.DictReader(csvfile, fieldnames)
        next(reader) #the first row is fieldnames
        nodes = []
        links = []

        for row in reader:
            CF = eval(row['CF'])
            ID = row['ID']
            nodes.append({"Id":ID, "name":row['Name'], "TF":row['TF'], "AUA":row['AUA'], "CF":CF, "MF":row['MF'], "FD":row['FD']})
            for idd in CF:
                links.append({"Source":ID,"Target":idd})

        json.dump({'nodes': nodes,'links': links},jsonfile)

        csvfile.close()
        jsonfile.close()

        return render_template('showGraph.html')
@app.route('/', methods=['POST'])
def handle_posts():
    if request.method == 'POST':
        if request.form["button"]=="Crawl":
            return crawl_facebook()

        elif request.form["button"]=="Upload":
            return upload_file()
        elif request.form["button"]=="CrawlTwitter":
            return crawl_twitter()
        elif request.form["button"]=="MoveToManuallyAddPage":
            return render_template('addManuallyPage.html')



if __name__ == '__main__':
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(debug=True)