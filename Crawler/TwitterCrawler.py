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
    "MAIL_USERNAME": "alexan.c09@gmail.com",
    "MAIL_PASSWORD": "15Po23G7"
}
app2.config.update(mail_settings)
mail = Mail(app2)

class TwitterCrawler:
    curr_name = 'AlexChinyan'
    my_id = 3283644367  # AlexChinyan

    def __init__(self):
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
        values = [user['id_str'], user['Name'] if self.english(user['name']) else user['screen_name'], user['friends_count'], MF,
                  self.fix_date(user['created_at']), FD, CF]  # needs to change created_at to months
        # if my_file.loc[my_file['ID'] == user['id_str']]:
        #     my_file.loc[my_file['ID'] == user['id_str']] = values
        # else:
        self.my_file.loc[len(self.my_file)] = values

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
            with open('second_circle.txt', 'w') as filehandle:
                filehandle.writelines("%s\n" % place for place in self.second_circle)
            with open('second_to_scan.txt', 'w') as filehandle:
                filehandle.writelines("%s\n" % place for place in self.second_to_scan)
            with open('to_scan.txt', 'w') as filehandle:
                filehandle.writelines("%s\n" % place for place in self.to_scan)

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
        curr_name = uname

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

# -- ! TODO ! --
# change file name
# add try & catch
# open email address for this app
# trying to scan someone that already been scanned
# show twitter graph ?


