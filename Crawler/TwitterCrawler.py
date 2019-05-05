import sys, logging
import string, csv, time, os
from twython import Twython
import pandas as pd

curr_name = 'AlexChinyan'
fieldnames = ['ID', 'Name', 'TF', 'MF', 'AUA', 'FD', 'CF']
my_file = None
my_id = 3283644367  # AlexChinyan
first_circle = []
second_circle = []
to_scan = []
second_to_scan = []
ego_user = ''
logger = ''
twitter = ''


def init_crawler():
    access_token = "1095610485603479552-uk9jpfQB8WMUQ9KpuGaKogN3T0rXdT"
    access_token_secret = "LutHGO95xCy7OYsblJ7S7L4UNR2EY3cNHUvhQ2cdDADZX"
    consumer_key = "uMD4HfVrPA8OXu9OAosFQKnu7"
    consumer_secret = "cBDNg3oCxkL2kL4ap4088qpsrhx4JHbuDQ319irgFYOE9BcyPP"

    return Twython(app_key=consumer_key, app_secret=consumer_secret, oauth_token=access_token,
                   oauth_token_secret=access_token_secret)


def init_csv():
    global my_file
    path_name = curr_name + "_27/4_data.csv"

    my_file = pd.read_csv(path_name) if os.path.isfile("./" + path_name) else pd.DataFrame(columns=fieldnames)

    return


def init_logger():
    global logger

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)-5.5s]  %(message)s",
        handlers=[logging.FileHandler('./logger.log'), ])
    logger = logging.getLogger('twitter_crawler')

    return


def export_to_csv(name):
    # remove second row from my_file

    my_file.to_csv(name)
    return


def english(str):
    return (any("\u0590" <= c <= "\u05EA" for c in str) == []) and str[0].isalpha()


def fix_date(date):
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


def add_to_csv(user, MF, FD, CF):
    if MF == -1: MF = user['followers_count']
    values = [user['id_str'], user['Name'] if english(user['name']) else user['screen_name'], user['friends_count'], MF,
              fix_date(user['created_at']), FD, CF]  # needs to change created_at to months
    # if my_file.loc[my_file['ID'] == user['id_str']]:
    #     my_file.loc[my_file['ID'] == user['id_str']] = values
    # else:
    my_file.loc[len(my_file)] = values

    logger.info('added ' + str(values) + ' to csv file.')
    return


def add_ego_node(ego_user):
    ego_user = ego_user
    ego_user['id_str'] = str(0)  # the ego_node has id = 0
    add_to_csv(ego_user, 0, 0, [])
    logger.info('added ego_node to csv.')
    return


def handle(e):
    logger.error('got an error ' + str(e))
    if '429' in str(e):
        logger.info('save and stop')
        with open('second_circle.txt', 'w') as filehandle:
            filehandle.writelines("%s\n" % place for place in second_circle)
        with open('second_to_scan.txt', 'w') as filehandle:
            filehandle.writelines("%s\n" % place for place in second_to_scan)
        with open('to_scan.txt', 'w') as filehandle:
            filehandle.writelines("%s\n" % place for place in to_scan)

        time.sleep(911)
    elif '403' in str(e):
        # change to cases according to error number
        ## in case of twitter timeout we need to wait 15min=900sec

        export_to_csv(curr_name + "_data.csv")

    return


def scan_user(users, cf, arr_scan, arr_circ):
    cursor = -1  # restart cursor

    for entry in users:
        uname = entry['screen_name']
        amount = min(entry['friends_count'], 1200)
        if cf == []: cf = [entry['id_str']]
        add_to_csv(entry, -1, -1, ['0'])
        msg = 'crawling: ' + uname + ' , num of friends: ' + str(amount)
        logger.info(msg)

        while cursor != 0 and amount > 0:
            try:
                following = twitter.get_friends_list(screen_name=uname, cursor=cursor, count=min(200, amount))
                for u in following["users"]:
                    add_to_csv(u, -1, -1, cf)  # at first we try to add to CSV
                    # no exception was raised from CSV
                    if u['friends_count'] < 1200:
                        arr_scan.append(u["id_str"])
                        arr_circ.append(u["id_str"])

                cursor = following["next_cursor"]  # iterator = next
            except Exception as e:
                handle(e)
                continue

            amount -= 200

        cursor = -1  # restart cursor
        cf = []

    return

def run(uname):
    global to_scan,first_circle,second_to_scan,second_circle,twitter

    ##start##
    twitter = init_crawler()
    init_logger()
    init_csv()
    logger.info('starting crawling')
    print('starting crawling')

    # us = twitter.lookup_user(user_id=str(my_id))
    us = twitter.lookup_user(screen_name=uname)
    logger.info('got data about ego_node')
    add_ego_node(us[0])

    # first_circle"
    scan_user(us, ['0'], to_scan, first_circle)
    # export_to_csv(curr_name + "_data.csv")
    print('after scanning first circle')
    print('number of people to scan: ', len(to_scan))

    ### second_circle ###

    while len(to_scan) != 0:
        ids = ''
        for i in range(0, min(100, len(to_scan))):
            ids = ids + to_scan[i] + ', '
        ids = ids[:-2]  # remove last ', '
        res = twitter.lookup_user(user_id=ids)
        scan_user(res, [], second_to_scan, second_circle)
        to_scan = to_scan[i:]
        if i == 0: break;

    logger.info('finish crawling')
    print('done')
    export_to_csv(curr_name + "_27/4_data.csv")
