import sys, logging
import string, csv, time, os
from twython import Twython
import pandas as pd
# send file to mailAddress
from flask import Flask
from flask_mail import Mail, Message

app2 = Flask(__name__)  # app2 = Flask(__name__, static_folder='./media')
mail_settings = {
    "MAIL_SERVER": 'smtp.gmail.com',
    "MAIL_PORT": 465,
    "MAIL_USE_TLS": False,
    "MAIL_USE_SSL": True,
    "MAIL_USERNAME": "IFCMproject@gmail.com",
    "MAIL_PASSWORD": "IFCM2019"
}
app2.config.update(mail_settings)
mail = Mail(app2)

class TwitterCrawler:
    # curr_name = 'AlexChinyan',  my_id = 3283644367  # AlexChinyan

    def __init__(self,anonymCB):
        self.my_file = None
        self.fieldnames = ['ID', 'Name', 'TF', 'MF', 'AUA', 'FD', 'CF']
        self.first_circle = []
        self.second_circle = []
        self.to_scan = []
        self.second_to_scan = []
        self.ego_user = ''
        self.logger = ''
        self.twitter = ''
        self.path_name = ''
        self.curr_name = ''
        self.anonymCB = anonymCB

    def init_crawler(self):
        access_token = "1095610485603479552-uk9jpfQB8WMUQ9KpuGaKogN3T0rXdT"
        access_token_secret = "LutHGO95xCy7OYsblJ7S7L4UNR2EY3cNHUvhQ2cdDADZX"
        consumer_key = "uMD4HfVrPA8OXu9OAosFQKnu7"
        consumer_secret = "cBDNg3oCxkL2kL4ap4088qpsrhx4JHbuDQ319irgFYOE9BcyPP"

        return Twython(app_key=consumer_key, app_secret=consumer_secret, oauth_token=access_token,
                       oauth_token_secret=access_token_secret)

    def init_csv(self,uname):

        outname = uname + ".csv"
        outdir = os.path.join( os.getcwd(), 'csvfiles')

        if not os.path.exists(outdir):
            os.mkdir(outdir)

        self.path_name = os.path.join(outdir, outname)

        self.my_file = pd.read_csv(self.path_name) if os.path.isfile(self.path_name) else pd.DataFrame(columns=self.fieldnames)

        return

    def init_logger(self):
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s [%(levelname)-5.5s]  %(message)s",
            handlers=[logging.FileHandler('./logger.log'), ])
        self.logger = logging.getLogger('twitter_crawler')

        return

    def export_to_csv(self,name):
        # remove second row from my_file

        self.my_file.to_csv(name)

        return

    def english(self,str):
        return (any("\u0590" <= c <= "\u05EA" for c in str) == []) and str[0].isalpha()

    def fix_date(self,date):
        # Sun Apr 10 15:56:52 +0000 2016

        from datetime import datetime
        now = datetime.now()

        date = date.split(' ')
        st = date[1] + ' ' + date[2] + ' ' + date[5]

        d1 = datetime.strptime(st, '%b %d %Y')
        d2 = now.strftime("%b %d, %Y")
        d2 = d2.replace(",", "")
        d2 = datetime.strptime(d2, '%b %d %Y')

        return abs((d2 - d1).days)

    def add_to_csv(self,user, MF, FD, CF):
        if user['screen_name'] == self.curr_name : return
        if MF == -1: MF = user['followers_count']
        name = user['name']

        values = {'ID': user['id_str'],'Name':name if self.english(user['name']) else user['screen_name'],'TF': user['friends_count'],'MF': MF, 'AUA' : self.fix_date(user['created_at']),
                  'FD': FD, 'CF':CF}

        self.my_file = self.my_file.append(values, ignore_index=True)

        self.logger.info('added ' + str(values) + ' to csv file.')
        return

    def add_ego_node(self,ego_user):
        ego_user = ego_user
        ego_user['id_str'] = str(0)  # the ego_node has id = 0
        self.add_to_csv(ego_user, 0, 0, [])
        self.logger.info('added ego_node to csv.')
        return

    def handle(self,e):
        self.logger.error('got an error ' + str(e))
        if '429' in str(e):
            self.logger.info('save and stop')

            time.sleep(911)
        elif '403' in str(e):
            # change to cases according to error number
            ## in case of twitter timeout we need to wait 15min=900sec

            self.export_to_csv(self.curr_name + "_data.csv")

        return

    def scan_user(self,users, cf, arr_scan, arr_circ):
        cursor = -1  # restart cursor

        for entry in users:
            uname = entry['screen_name']

            amount = min(entry['friends_count'], 1200)
            if cf == []: cf = [entry['id_str']]
            self.add_to_csv(entry, -1, -1, ['0'])
            msg = 'crawling: ' + uname + ' , num of friends: ' + str(amount)
            self.logger.info(msg)

            while cursor != 0 and amount > 0:
                try:
                    following = self.twitter.get_friends_list(screen_name=uname, cursor=cursor, count=min(200, amount))
                    for u in following["users"]:
                        self.add_to_csv(u, -1, -1, cf)  # at first we try to add to CSV
                        # no exception was raised from CSV
                        if u['friends_count'] < 1200:
                            arr_scan.append(u["id_str"])
                            arr_circ.append(u["id_str"])

                    cursor = following["next_cursor"]  # iterator = next
                except Exception as e:
                    self.handle(e)
                    continue

                amount -= 200

            cursor = -1  # restart cursor
            cf = []

        return

    def run(self,uname,mailAddress):
        self.curr_name = uname

        #open thread with promise
        import threading
        t1 = threading.Thread(target=self.scan(uname,mailAddress))
        t1.start()

        return

    def scan(self,uname,mailAddress):
        ##start##
        self.twitter = self.init_crawler()
        self.init_logger()
        self.init_csv(uname)
        self.logger.info('starting crawling')
        print('starting crawling')

        # us = twitter.lookup_user(user_id=str(my_id))
        us = self.twitter.lookup_user(screen_name=uname)
        self.logger.info('got data about ego_node')
        self.add_ego_node(us[0])

        # first_circle"
        self.scan_user(us, ['0'], self.to_scan, self.first_circle)
        # export_to_csv(curr_name + "_data.csv")
        print('after scanning first circle')
        print('number of people to scan: ', len(self.to_scan))

        ### second_circle ###

        while len(self.to_scan) != 0:
            ids = ''
            for i in range(0, min(100, len(self.to_scan))):
                ids = ids + self.to_scan[i] + ', '
            ids = ids[:-2]  # remove last ', '
            res = self.twitter.lookup_user(user_id=ids)
            self.scan_user(res, [], self.second_to_scan, self.second_circle)
            self.to_scan = self.to_scan[i:]
            if i == 0: break;

            self.logger.info('finish crawling')
        print('done')

        self.my_file = self.my_file.drop_duplicates(subset='ID')

        self.export_to_csv(self.path_name)

        from AlgorithmSolver.AlgorithmSolver import AlgorithmSolver

        algSolv = AlgorithmSolver(self.path_name, 0.03)
        algSolv.generate(False)
        algSolv.add_ego_node()
        fields = self.fieldnames
        fields.append('TSP')

        import ast

        df = pd.DataFrame(columns=fields)
        for key, node in algSolv.nodes.items():
            values = {'ID': node.idd, 'Name': node.name,
                      'TF': node.tf, 'MF': node.mf, 'AUA': node.aua,
                      'FD': node.fd, 'CF': node.cf, 'TSP': node.tsp}
            df = df.append(values,ignore_index=True)

        if self.anonymCB:
            try:
                df['Name'] = list(map(EncryptionCSV.encName, df['Name'].values.tolist()))
            except Exception as e:
                print(e)

        self.my_file = df
        self.export_to_csv(self.path_name)

        with app2.app_context():
            with app2.open_resource(self.path_name) as fp:
                msg = Message(subject="Hello",
                              sender=app2.config.get("MAIL_USERNAME"),
                              recipients=[mailAddress],  #email
                              body = "This is a test email I sent with Gmail and Python!"
                              )
                msg.attach(
                    self.path_name,
                    'application/octect-stream',
                    fp.read())
            mail.send(msg)
        os.remove(self.path_name)

# -- ! TODO ! --
# @minchal70
# open email address for this app


class EncryptionCSV:
    def encName(str):
        arraysplitted = str.split('.')
        strEnc=""
        for s in arraysplitted:
            strEnc=strEnc+s[0]+'.'
        return strEnc[0:len(strEnc)-1];

    def addNumOfSameNames(listOfEncName):
        tempList=listOfEncName
        counterOut=0
        for i in tempList:
            sumof=1
            counter=counterOut
            if(i[i._len_()-2]!='#'):
                for r in listOfEncName[counterOut:listOfEncName._len_()]:
                    if(r==i):
                        listOfEncName[counter]=listOfEncName[counter]+'#'+str(sumof)
                        sumof=sumof+1
                    counter=counter+1
            counterOut=counterOut+1
        return listOfEncName
