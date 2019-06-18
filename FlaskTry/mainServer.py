from time import sleep
from logos import *
from flask import Flask, render_template, request, redirect, send_from_directory, send_file
from AlgorithmSolver import createJson as cJson
from Crawler.TwitterCrawler import TwitterCrawler
from Crawler.FBCrawler import FBCrawler
import os
import json
import math
import threading
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


def writeToLog(text):
    f = open("loggerForWeb.log", "a")
    f.write(text + "\n")
    f.close()

def deleteLogFile():
    with open("loggerForWeb.log", 'w') as file:
        file.write('')

class myThread (threading.Thread):
    """
    Thread class which each one execute part of first circle friends and all their second circle friends.
    """
    def __init__(self, facebook_crawler, threadID, name, paths):
        threading.Thread.__init__(self, name=name)
        self.facebook_crawler = facebook_crawler
        self.threadID = threadID
        self.name = name
        self.paths = paths


    def run(self):
        #logger.info("Starting work on thread: " + self.name)
        for path in self.paths:
            self.facebook_crawler.crawl_data_of_user_friends(path, self.threadID)
        #logger.info("Finished work on thread: " + self.name)

@app.route('/database_download/<filename>')
def database_download(filename):
    return send_from_directory('data', filename)

def crawl_facebook():
    writeToLog(FBCrawler_LOGO)
    writeToLog("*" * 100)
    email = request.form['emailForFacebook']
    password = request.form['passwordForFacebook']
    fbc = FBCrawler("FromWebSite")
    writeToLog('Facebook crawler module initialized!')
    writeToLog("*" * 100)
    #fbc.run_selenium_browser()
    csv_file_name = fbc.initiate_csv_file()
    writeToLog('Try to log in to Facebook...')
    session_cookies, session = fbc.login_to_facebook(email, password)
    if not session_cookies and not session:
        writeToLog('Could not login to facebook! :(\nPlease Check your email and password..')
        deleteLogFile()
        return render_template('index.html', errorFBC="Incorrect Email or password", scroll="crawlFacebook")
    writeToLog('Successfully Logged in!')
    try:
        fbc.get_facebook_username(session_cookies, session)
    except Exception:
        deleteLogFile()
        return render_template('index.html', errorFBC="Crawling encountered issue, check connectivity to Facebook user", scroll="crawlFacebook")

    writeToLog('Start to get first circle data..')
    try:
        first_circle_initial_data_folder, num_of_pages = fbc.get_user_first_circle_friends_initial_scan_data(
            session_cookies,
            session)
    except Exception:
        deleteLogFile()
        return render_template('index.html', errorFBC="Crawling encountered issue in first circle, check connectivity to Facebook user",
                               scroll="crawlFacebook")
    writeToLog('Finished to get first circle data!')

    try:
        config, utils = fbc.get_config_and_utils()
        num_of_threads = math.ceil(num_of_pages / config.getint('General', 'num_of_json_per_thread'))
        paths_for_each_thread = utils.get_paths_for_each_thread(first_circle_initial_data_folder,
                                                                config.getint('General', 'num_of_json_per_thread'))

        fbc.initiate_osn_dicts_and_sessions(num_of_threads, email, password)

        threadList = []
        for i in range(0, num_of_threads):
            threadList.append('Thread-' + str(i))

        i = 0
        threads = []
        writeToLog('Start to work on second level data.. This will take a while..')
        for tName in threadList:
            thread = myThread(fbc, i, tName, paths_for_each_thread[i])
            thread.start()
            threads.append(thread)
            i += 1

        for t in threads:
            t.join()
        path_to_csv = fbc.arrange_csv_file_from_mid_data(fbc.json_files_folder, 'data/' + csv_file_name)

    except Exception:
        deleteLogFile()
        return render_template('index.html', errorFBC="Crawling encountered issue in Second circle, check connectivity to Facebook user",
                               scroll="crawlFacebook")

    writeToLog('Finished to work on second level data!')
    full_path_to_csv = os.path.join(os.getcwd(), path_to_csv)

    writeToLog('Got all possible data.. Generating final graph.')
    try:
        cJson.create(full_path_to_csv, 1)
    except Exception:
        deleteLogFile()
        return render_template('index.html', errorFBC="Encountered issue in Graph generation..", scroll="crawlFacebook")

    writeToLog('Finished to generate final graph.. Moving to graph presentation')
    deleteLogFile()
    return render_template('showGraph.html', filename=csv_file_name)

def crawl_twitter():
    writeToLog(TwitterCrawler_LOGO)
    nick_name = request.form['twitterName']
    mail_for_results = request.form['emailForResults']
    nick_name = nick_name[1:]
    writeToLog("Start to work on Twitter user: " + nick_name)
    writeToLog("Result CSV file will be sent to :" + mail_for_results)
    tc = TwitterCrawler()
    try:
        tc.run(nick_name,mail_for_results)
    except Exception as e:
        deleteLogFile()
        return render_template('index.html', errorTWIC="Error while crawling Twitter, Please try again later.", scroll="crawlTwitter")
    deleteLogFile()
    return render_template('index.html', messageForTweetCrawler="CSV file sent to: " + mail_for_results)

def upload_file():
    writeToLog(UPLOAD_CSV_LOGO)
    # check if the post request has the file part
    if 'file' not in request.files:
        deleteLogFile()
        return render_template('index.html', errorFBU="No file selected", scroll="uploadFacebook")

    file = request.files['file']
    ext = [".csv", ".xls", ".xlsx"]
    if file:
        if not file.filename.lower().endswith(tuple(ext)):
            deleteLogFile()
            return render_template('index.html', errorFBU="Please upload CSV file.", scroll="uploadFacebook")
        path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(path)
        if(os.stat(path).st_size > 1000000):
            writeToLog("This is a large CSV file.. will show only bad connections")
            toBig = True
        else:
            toBig = False
        tsp = request.form['tspFCBNum']

        try:
            writeToLog("Start to evaluate the OSN graph according uploaded CSV..")
            writeToLog("This can take a while...")
            if tsp=='':
                writeToLog("Using default TSP: 0.03")
                cJson.create(path, 1, toBig)

            else:
                writeToLog("Choosen TSP: " + tsp)
                cJson.create(path, 1, toBig, float(tsp))
        except Exception:
            deleteLogFile()
            return render_template('index.html', errorFBU="Error while parsing CSV file", scroll="uploadFacebook")
        deleteLogFile()
        return render_template('showGraph.html')

def upload_twitter_file():
    # check if the post request has the file part
    if 'file' not in request.files:
        return redirect(request.url)
    file = request.files['file']
    if file:
        path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(path)
        return render_template('showGraph.html')

@app.route('/', methods=['POST'])
def handle_posts():
    try:
        if request.method == 'POST':
            if request.form["button"] == "Crawl":
                return crawl_facebook()
            elif request.form["button"] == "Upload":
                return upload_file()
            elif request.form["button"] == "CrawlTwitter":
                return crawl_twitter()
            elif request.form["button"] == "MoveToManuallyAddPage":
                return render_template('addManuallyPage.html')
            elif request.form["button"] == 'UploadTwitter':
                return upload_twitter_file()
    except:
        return render_template('index.html')

    return render_template('index.html')


@app.route('/stream')
def stream():
    def generate():
        with open('loggerForWeb.log', 'r') as f:
            while True:
                yield f.read()
                sleep(1)

    return app.response_class(generate(), mimetype='text/plain')


if __name__ == '__main__':
    deleteLogFile()
    app.jinja_env.auto_reload = True
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(debug=True)
