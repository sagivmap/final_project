from bs4 import BeautifulSoup
from selenium import webdriver
from Crawler.utils import utils
from logging.config import fileConfig
import requests
import configparser
import re
import os
import logging
import threading
import math

import time

# initiate config file
config = configparser.ConfigParser()
config.read('C:/Users/sagiv/PycharmProjects/ProjectTry/Crawler/config/config.ini')

# initiate logger
fileConfig('C:/Users/sagiv/PycharmProjects/ProjectTry/Crawler/config/logger_config.ini')
fh = logging.FileHandler('main.log')
formatter = logging.Formatter('%(asctime)s - %(threadName)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
logger = logging.getLogger()
logger.addHandler(fh)

utils = utils(logger)

class FBCrawler:
    def __init__(self, run_id):
        self.run_id = run_id
        self.csv_file_name = ''
        self.osn_data = {}
        self.osn_data_lock = threading.Lock()

        self.osn_data_as_list = []
        self.session_and_cookies = []
        self.exception_thrown = []
        self.json_files_folder = 'first_and_second_data_raw/' + self.run_id + '_' + utils.get_timestamp()
        os.makedirs(self.json_files_folder)


    def initiate_csv_file(self):
        """
        initiate the CSV that will contain the input data for the main algorithm
        :param file_name_prefix: requested name to the csv file
        :return: csv final name (+ timestamp for avoid overloading)
        """
        logger.info('Start to initiate the csv file')
        columns = ['ID', 'Name', 'TF', 'MF', 'AUA', 'FD', 'CF']
        csv_file_name = self.run_id + '_' + utils.get_timestamp() + '.csv'
        utils.write_row_in_csv_file('data/'+csv_file_name, columns)
        logger.info('Finished to initiate the csv file: ' + csv_file_name)
        self.csv_file_name = csv_file_name
        return csv_file_name


    def login_to_facebook(self, email=config.get('LoginDetails', 'email'), password=config.get('LoginDetails', 'pass')):
        """
        login to Facebook according credentials in config.ini
        :return: session cookies, session
        """
        self.osn_data_lock.acquire()
        logger.info('Start to login to Facebook.')
        # login page url
        url = config.get('LoginDetails', 'login_url')
        # initiating the session
        try:
            s = requests.session()
            # login data
            post_data = {
                'email': email,
                'pass': password,
            }
            attempts_num = config.getint('LoginDetails', 'try_amount')
            for i in range(attempts_num):
                # post the login data
                r = s.post(url, data=post_data, allow_redirects=False)
                soup = BeautifulSoup(r.text, features="html.parser")
                if r.status_code == 302:
                    flag, r = utils.customized_get_request(r._next.url, s, r.cookies, 1)
                    if "התחבר" in r.text:
                        logger.error('Could not login in: ' + str(i) + '/' + str(attempts_num))
                    else:
                        logger.info('Successfully logged in to Facebook.')

                        self.osn_data_lock.release()
                        return r.cookies, s
                else:
                    logger.error('Could not login in: ' + str(i)+ '/' +str(attempts_num))

            logger.error('Failed to log in!')
            if s: s.close()
            self.osn_data_lock.release()
            return None, None
        except Exception as e:
            logger.error('Failed to log in!')
            self.osn_data_lock.release()
            return None, None

    def run_selenium_browser(self):
        browser = webdriver.Firefox()
        browser.get('https://m.facebook.com/friends/center/friends/')

    def get_user_first_circle_friends_initial_scan_data(self, cookies, session):
        """
        Method that scrape the logged in user's friend list and get their ID for later processing
        :param cookies: cookies of logged in session
        :param session: logged in session
        :param output_filename: desired output name
        :return: output_filename + timestamp
        """
        json_files_folder = 'first_circle_initial_data/'+self.run_id+'_' + utils.get_timestamp()
        os.makedirs(json_files_folder)

        logger.info('Start to crawl user\'s initial friend list for getting friend id, name and MF')
        i = 0
        while True:
            users_friends_first_scan_data = []
            logger.info('Start to work on page: ' + str(i))
            attempt_num = config.getint('UserFriendsList', 'try_amount')
            succeed_to_get, r = utils.customized_get_request(config.get('UserProfile', 'path_to_friends') +
                          '?' + config.get('UserProfile', 'friends_list_first_key') + '=' + str(i) +
                          '&' + config.get('UserProfile', 'friends_list_second_key') + '=' +
                                config.get('UserProfile', 'friends_list_second_value') +
                          '&' + config.get('UserProfile', 'friends_list_first_key') + '=' + str(i),
                                                             session, cookies, attempt_num)

            if not succeed_to_get:
                logger.error('Failed to Get friend page num: ' + str(i))
                i += 1
                continue

            soup = BeautifulSoup(r.text, 'html.parser')

            friend_tag_list = soup.findAll('td', class_=config.get('UserFriendsList', 'friend_row_td_class'))
            if not friend_tag_list:
                logger.info('Reached to last page of friend list')
                break
            for friend in friend_tag_list:
                friend_dict = {}
                friend_a_tag = friend.find('a', class_=config.get('UserFriendsList', 'friend_row_a_class'))
                # Get friend's id
                link = friend_a_tag['href']
                friend_dict['friend_id'] = re.search(r'\?uid=(\d+)', link).group(1)
                logger.info('Get data of: ' + friend_a_tag.text)
                # Get Friend's name
                friend_dict['friend_name'] = friend_a_tag.text
                friend_mutual_friends_text = friend.find('div', class_=config.get('UserFriendsList',
                                                                                  'friend_row_div_class_mf')).text
                # Get Mutual friends
                amount_of_mutual_friends = re.search(r'(\d+)', friend_mutual_friends_text)
                if amount_of_mutual_friends:
                    friend_dict['friend_mutual_friends'] = re.search(r'(\d+)', friend_mutual_friends_text).group(1)
                else:
                    friend_dict['friend_mutual_friends'] = '0'

                friend_dict['connecting_friend_id'] = '0'
                users_friends_first_scan_data.append(friend_dict)

            utils.save_to_json_file_no_TS(users_friends_first_scan_data, json_files_folder + '/' + str(i))

            logger.info('Finished to work on page: ' + str(i))
            i += 1

        logger.info('Finished to work on getting user\'s initial Friends list, stored data in:' + json_files_folder)
        return json_files_folder, i

    def _get_friendship_duration_as_months(self, soup):
        """
        helper function which get friendship duration as text represented in FB
        :param soup: soup object of friendship page
        :return:
        """
        friendship_info_tags = soup.findAll(lambda tag: tag.name == 'td' and re.match(r'Your friend since (\w{3,9} \d{4})', tag.text))
        for info_tag in friendship_info_tags:
            ans = re.search(r'Your friend since (\w{3,9} \d{4})',info_tag.text)
            if ans:
                return utils.convert_friendship_duration_text_to_month(ans.group(1))

        friendship_info_tags = soup.findAll(lambda tag: tag.name == 'td' and re.match(r'Your friend since (\w{3,9})', tag.text))
        for info_tag in friendship_info_tags:
            ans = re.search(r'Your friend since (\w{3,9})',info_tag.text)
            if ans:
                return utils.convert_only_month_friendship_duration_text_to_month(ans.group(1))


    def __add_data_to_main_structure(self, id, name, tf, mf, aua, fd, cf, thread_id):
        """
        function that add to thread_id DS the first\second circle's friend
        :param id:
        :param name:
        :param tf:
        :param mf:
        :param aua:
        :param fd:
        :param cf:
        :param thread_id:
        :return:
        """
        self.osn_data_as_list[thread_id][id] = {'Name':name,
                             'TF': tf,
                             'MF': mf,
                             'AUA': aua,
                             'FD': fd,
                             'CF': cf,}

    def __get_new_session_for_thread(self, thread_id):
        """
        if session is corrupted so re-login to facebook
        :param thread_id:
        :return:
        """
        logger.info("Re-Login to facebook")
        cookies, session = self.login_to_facebook()
        while (cookies is None) and (session is None):
            cookies, session = self.login_to_facebook()
        self.session_and_cookies[thread_id] = session, cookies


    def __get_friendship_duration_from_friend_id(self, friend_id, thread_id):
        """
        function which crawl from facebook the friendship duration of user and one of his first circle friends
        :param friend_id: friend's facebook id (extracted in phase 1)
        :param thread_id:
        :return: friendship duration
        """
        attempt_num = config.getint('FriendshipDuration', 'try_amount')
        url = config.get('FriendshipDuration', 'friendship_link') + friend_id

        while True:
            succeed_to_get, r = utils.customized_redirected_get_request(url, self.session_and_cookies[thread_id][0],
                                                                        self.session_and_cookies[thread_id][1], attempt_num)
            if succeed_to_get:
                break
            if config.get('General','page_to_ignore_text') in r.text:
                return None
            if (config.get('General','page_not_found_msg') in r.text and r.status_code == 404) or r.status_code == 500:
                return None
            else:
                time.sleep(30)
                self.__get_new_session_for_thread(thread_id)



        soup = BeautifulSoup(r.text, 'html.parser')
        friendship_duration_as_months = self._get_friendship_duration_as_months(soup)

        return friendship_duration_as_months

    def __get_num_of_days_since_earliest_post_from_timeline(self, uri_to_year_timeline, thread_id):
        """
        extract the date of the first post that user posted and count the day since then
        :param uri_to_year_timeline:
        :param thread_id:
        :return: days since first post
        """
        if uri_to_year_timeline.startswith('http'):
            url = uri_to_year_timeline
        else:
            url = config.get('General', 'facebook_url') + uri_to_year_timeline
        while True:
            succeed_to_get, r = utils.customized_get_request(url, self.session_and_cookies[thread_id][0],
                                                             self.session_and_cookies[thread_id][1],
                                                             config.getint('UserAge', 'try_amount'))
            if succeed_to_get:
                break

            if (config.get('General','page_not_found_msg') in r.text and r.status_code == 404) or r.status_code == 500:
                return None

            else:
                logger.error('Could not GET year timeline in uri: ' + uri_to_year_timeline)
                time.sleep(30)
                self.__get_new_session_for_thread(thread_id)

        soup = BeautifulSoup(r.text, 'html.parser')
        all_posts_dates_tags = list(reversed(soup.findAll('abbr')))
        if not all_posts_dates_tags:
            return None

        return utils.get_num_of_days_from_first_post_date(all_posts_dates_tags[0].text)


    def _get_FB_user_account_age_as_days(self, soup, thread_id):
        """
        This function finds the earliest year after 2004 (facbook foundation) and search for the first post as
        indication for user initialization and counts the days from now to then
        :param soup: soup of timeline user's page
        :param thread_id:
        :return: FB user age as days
        """
        timeline_year_tags = soup.findAll(lambda tag: tag.name == 'div' and re.match(r'^\d{4}$', tag.text) and tag.find('a'))
        timeline_year_tags = list(reversed(list(filter(lambda x: x.find('a'), timeline_year_tags))))
        for year_tag in timeline_year_tags:
            if int(year_tag.text) >= 2004:
                days_since_joined = self.__get_num_of_days_since_earliest_post_from_timeline(year_tag.find('a')['href'],
                                                                                             thread_id)

                if days_since_joined:
                    return days_since_joined

                else:
                    return utils.get_days_since_start_of_year(year_tag.text)

        # if all years tags are empty from posts
        for year_tag in timeline_year_tags:
            if int(year_tag.text) >= 2004:
                return utils.get_days_since_start_of_year(year_tag.text)


    def __get_friend_friend_list_uri(self, soup):
        """
        Extract a link to friend list page from the soup of timeline page
        :param soup:
        :return:
        """
        uris_include_friend_text = soup.findAll(lambda tag: tag.name == 'a' and re.match(r'Friends', tag.text))
        if len(uris_include_friend_text)>1:
            return uris_include_friend_text[1]['href']
        return None

    def __get_facebook_user_account_age(self, facebook_user_id, thread_id, is_fs_friend=True):
        """
        function that gets the age of user acount in facebook
        :param facebook_user_id: facebook_user's facebook id
        :param thread_id:
        :param is_fs_friend: flag that tell if it first\second circle friend
        :return: age of user in days
        """
        attempt_num = config.getint('UserAge', 'try_amount')
        url = config.get('UserAge', 'user_age_link') + facebook_user_id
        while True:
            if is_fs_friend:
                succeed_to_get, r = utils.customized_redirected_get_request(url, self.session_and_cookies[thread_id][0],
                                                                            self.session_and_cookies[thread_id][1], attempt_num)
            else:
                succeed_to_get, r = utils.customized_get_request(url, self.session_and_cookies[thread_id][0],
                                                                    self.session_and_cookies[thread_id][1], attempt_num)
            if succeed_to_get:
                break

            if (config.get('General','page_not_found_msg') in r.text and r.status_code == 404) or r.status_code == 500:
                return None

            if config.get('General','page_to_ignore_text') in r.text:
                return None, None

            if not succeed_to_get:
                logger.error('Could not GET timeline page with: ' + facebook_user_id)
                time.sleep(30)
                self.__get_new_session_for_thread(thread_id)

        soup = BeautifulSoup(r.text, 'html.parser')
        facebook_user_facebook_age_in_days = self._get_FB_user_account_age_as_days(soup, thread_id)


        friend_friends_list_uri = self.__get_friend_friend_list_uri(soup)
        return facebook_user_facebook_age_in_days , friend_friends_list_uri


    def __get_facebook_user_amount_of_friends_from_first_friends_page(self, soup):
        """
        search the amount of a friends in user first first page of friends list
        :param soup:
        :return:
        """
        firends_amount_header = soup.find(lambda tag: tag.name == 'h3' and re.match(r'Friends \((\d+|\d+\,\d+)\)', tag.text))
        if firends_amount_header:
            return utils.get_amount_of_friends_from_text(firends_amount_header.text)


    def _get_facebook_user_amount_of_friends(self, facebook_user_friend_list_uri, thread_id):
        """
        Function which get the user's amount of friends in facebook
        :param facebook_user_friend_list_uri: facebook id of user
        :param thread_id:
        :return: amount of friends, soup of first page for later analyzing
        """
        url = config.get('General', 'facebook_url') + facebook_user_friend_list_uri
        while True:
            succeed_to_get, r = utils.customized_get_request(url, self.session_and_cookies[thread_id][0],
                                                             self.session_and_cookies[thread_id][1],
                                                             config.getint('UserFriendsAmount', 'try_amount'))
            if succeed_to_get:
                break

            if (config.get('General','page_not_found_msg') in r.text and r.status_code == 404) or r.status_code == 500:
                return None
            else:
                logger.error('Could not GET facebook user\'s first friends list page, at url: ' + facebook_user_friend_list_uri)
                time.sleep(30)
                self.__get_new_session_for_thread(thread_id)

        soup = BeautifulSoup(r.text, 'html.parser')
        facebook_user_amount_of_friends = self.__get_facebook_user_amount_of_friends_from_first_friends_page(soup)

        return facebook_user_amount_of_friends, soup

    def __get_sc_friend_data(self, tag, connecting_friend_id, thread_id):
        """
        concrete function which crawl the data of second circle friend
        :param tag: tag of second circle friend from first circle friend list of friends
        :param connecting_friend_id: connecting first circle friend
        :param thread_id:
        :return:
        """
        try:
            sc_friend_id = utils.get_sc_id_from_uri(tag.contents[0]['href'])
        except Exception as e:
            logger.error('Exception Thrown at utils.get_sc_id_from_uri: ' + str(e))


        sc_friend_name = tag.contents[0].text
        if re.match(r'^\d+$', sc_friend_id):
            try:
                sc_friend_user_age, uri_to_friends_list = self.__get_facebook_user_account_age(
                    config.get('SecondCircle', 'numeric_id_timeline_prefix') + sc_friend_id,
                    thread_id,
                    is_fs_friend=False)
            except Exception as e:
                logger.error("Exception Thrown at __get_facebook_user_account_age(1) at:" + connecting_friend_id +"\n"
                             +  str(e) + '\n' + tag.prettify())
                sc_friend_user_age, uri_to_friends_list = None, None
                self.exception_thrown[thread_id] = True
        else:
            try:
                sc_friend_user_age, uri_to_friends_list = self.__get_facebook_user_account_age(
                    sc_friend_id + config.get('SecondCircle', 'TimelineVar'), thread_id,
                    is_fs_friend=False)
            except Exception as e:
                logger.error("Exception Thrown at __get_facebook_user_account_age(2) at:" + connecting_friend_id +"\n"
                             +  str(e) + '\n' + tag.prettify())
                sc_friend_user_age, uri_to_friends_list = None, None
        try:
            if uri_to_friends_list:
                sc_friend_amount_of_friends, ignore_value = self._get_facebook_user_amount_of_friends(
                    uri_to_friends_list, thread_id)
            else:
                sc_friend_amount_of_friends = None
        except Exception as e:
            logger.error("Exception Thrown at __get_facebook_user_amount_of_friends at " + connecting_friend_id +" on:\n" + str(e) + '\n' + tag.prettify())
            sc_friend_amount_of_friends = None
        try:
            sc_friend_mutual_friends = utils.get_mutual_friend_from_text(tag.contents[1].text)
        except Exception as e:
            logger.error("Exception Thrown at get_mutual_friend_from_text at "+ connecting_friend_id +", on:\n" + str(e) + '\n' + tag.prettify())
            sc_friend_mutual_friends = None
        try:
            self.__add_data_to_main_structure(sc_friend_id, sc_friend_name, sc_friend_amount_of_friends,
                                              sc_friend_mutual_friends, sc_friend_user_age,
                                              None, [connecting_friend_id], thread_id)
        except Exception as e:
            logger.error("Exception Thrown at __add_data_to_main_structure at " + connecting_friend_id +" on:\n" + str(e) + '\n' + tag.prettify())


    def __get_soup_to_next_page_of_friends(self, uri_to_next_page_tag, thread_id):
        url = config.get('General', 'facebook_url') + uri_to_next_page_tag['href']
        while True:
            succeed_to_get, r = utils.customized_get_request(url, self.session_and_cookies[thread_id][0],
                                                             self.session_and_cookies[thread_id][1],
                                                             config.getint('SecondCircle', 'try_amount'))

            if succeed_to_get:
                break

            if (config.get('General','page_not_found_msg') in r.text and r.status_code == 404) or r.status_code == 500:
                return None
            else:
                logger.error(
                    'Could not GET facebook user\'s first friends list page, at url: ' + uri_to_next_page_tag['href'])
                time.sleep(30)
                self.__get_new_session_for_thread(thread_id)

        soup = BeautifulSoup(r.text, 'html.parser')
        return soup

    def __crawl_friend_list_of_friends(self, friend_id, soup, page_num, thread_id):
        """
        function that going over all friend's friends and get the relavant data on them
        :param friend_id: first circle friend id
        :param soup: soup of first page of friends list
        :param page_num: which page of friend's friends
        :param thread_id:
        :return:
        """
        logger.info(friend_id + ': Start to crawl data on SC friends. Page num: ' + str(page_num))
        if page_num==1:
            if not soup.find(lambda tag: tag.name == 'h3' and re.match(r'Friends \((\d+|\d+\,\d+)\)', tag.text)):
                logger.info(friend_id + "'s SC friends data is not public. Finished to work.")
                return

        all_friends_in_page_tags = soup.findAll(lambda tag: tag.name == 'a' and tag.text == 'Add Friend')
        all_friends_in_page_tags = [tag.parent.parent for tag in all_friends_in_page_tags]
        for tag in all_friends_in_page_tags:
            try:
                self.__get_sc_friend_data(tag, friend_id, thread_id)
            except Exception as e:
                logger.error(str(e))

        logger.info(friend_id + ': Finished to crawl data on SC friends. Page num: ' + str(page_num))

        # get next page soup
        uri_to_next_page_tag = soup.find(lambda tag: tag.name == 'a' and tag.text == 'See More Friends')

        if uri_to_next_page_tag:
            soup_to_next_page = self.__get_soup_to_next_page_of_friends(uri_to_next_page_tag, thread_id)
            self.__crawl_friend_list_of_friends(friend_id, soup_to_next_page, page_num+1, thread_id)

    def crawl_data_of_user_friends(self, initial_data_filename, thread_id):
        """
        main function which crawl data for each user's friends save the data in CSV file
        :param initial_data_filename: file name of first initial data of user's friends (extracted in phase 1)
        :param thread_id: num of current thread the running
        :return:
        """
        logger.info("Start to work on user's friend's page")
        initial_friends_data = utils.load_json_file(initial_data_filename)
        for friend in initial_friends_data:
            try:
                logger.info("Start to work on "+ friend['friend_name'] + "'s page")

                # get friendship duration of friend
                try:
                    friendship_duration = self.__get_friendship_duration_from_friend_id(friend['friend_id'], thread_id)
                except Exception as e:
                    logger.error('Exception thrown at __get_friendship_duration_from_friend_id of ' + friend['friend_name'] +'\n' + str(e))
                if not friendship_duration:
                    logger.error("Could not get friendship duration for " + friend['friend_name'])

                # get user account age of a friend
                try:
                    age_of_friend_acount, friend_friends_list_uri = self.__get_facebook_user_account_age(friend['friend_id'],
                                                                                                     thread_id)
                except Exception as e:
                    logger.error('Exception thrown at  __get_facebook_user_account_age of ' + friend['friend_name'] +'\n' + str(e))
                if not age_of_friend_acount:
                    logger.error("Could not get friend's Facebook age for " + friend['friend_name'])

                if friend_friends_list_uri:
                    friend['friend_id'] = utils.get_fc_id_from_uri(friend_friends_list_uri)

                # get friend amount of friends
                try:
                    if friend_friends_list_uri:
                        friend_amount_of_friends, first_friends_list_soup = self._get_facebook_user_amount_of_friends(
                            friend_friends_list_uri, thread_id)
                    else:
                        friend_amount_of_friends, first_friends_list_soup = None, None
                except Exception as e:
                    logger.error('Exception thrown at  __get_facebook_user_amount_of_friends of ' + friend['friend_name'] +'\n' + str(e))
                if not friend_amount_of_friends:
                    logger.error("Could not get friend's amount of friends for " + friend['friend_name'])

                # add to main data structure
                self.__add_data_to_main_structure(friend['friend_id'], friend['friend_name'], friend_amount_of_friends,
                                                    int(friend['friend_mutual_friends']), age_of_friend_acount,
                                                    friendship_duration, list('0'), thread_id)

                # get second circle of user's direct friend (without MF)
                if first_friends_list_soup:
                    self.__crawl_friend_list_of_friends(friend['friend_id'], first_friends_list_soup, 1, thread_id)
                else:
                    logger.error("First friend's list soup is None, didn't crawl SC friends")


                utils.save_to_json_file(self.osn_data_as_list[thread_id], self.json_files_folder+'/'+friend['friend_id'])

                self.osn_data_as_list[thread_id] = {}

                logger.info("Finished to work on " + friend['friend_name'] + "'s page")

            except Exception as e:
                logger.error(e)

    def initiate_osn_dicts_and_sessions(self, num_of_threads):
        """
        initiate data structure for each thread so there won't be a race contidion
        :param num_of_threads: num of threads to initiate DS to.
        :return: None
        """
        for i in range(0, num_of_threads):
            self.osn_data_as_list.append({})
            cookies, session = self.login_to_facebook()
            while (cookies is None) and (session is None):
                cookies, session = self.login_to_facebook()
            self.session_and_cookies.append((session, cookies))
            self.exception_thrown.append(False)


    def arrange_csv_file_from_mid_data(self, path_to_mid_data_jsons_folder, path_to_csv_file):
        json_files = utils.get_all_json_files_in_path(path_to_mid_data_jsons_folder)
        for json_file in json_files:
            json_data = utils.load_json_file(os.path.join(path_to_mid_data_jsons_folder,json_file))
            for fb_id, fb_data in json_data.items():
                if fb_id in self.osn_data.keys():
                    self.osn_data[fb_id]['CF'].extend(fb_data['CF'])
                else:
                    self.osn_data[fb_id] = fb_data

        rows = []
        for id, data in self.osn_data.items():
            row = [id, data['Name'].encode('utf-8'), data['TF'], data['MF'], data['AUA'], data['FD'], data['CF']]
            rows.append(row)

        utils.write_rows_in_csv_file(path_to_csv_file, rows)

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
        logger.info("Starting work on thread: " + self.name)
        for path in self.paths:
            self.facebook_crawler.crawl_data_of_user_friends(path, self.threadID)
        logger.info("Finished work on thread: " + self.name)

if __name__ == "__main__":
    fbc = FBCrawler('omer_data')
    fbc.run_selenium_browser()
    csv_file_name = fbc.initiate_csv_file()
    session_cookies, session = fbc.login_to_facebook()
    while not session_cookies and not session:
        session_cookies, session = fbc.login_to_facebook()


    first_circle_initial_data_folder, num_of_pages = fbc.get_user_first_circle_friends_initial_scan_data(session_cookies,
                                                                                                 session)


    num_of_threads = math.ceil(num_of_pages / config.getint('General', 'num_of_json_per_thread'))
    paths_for_each_thread = utils.get_paths_for_each_thread(first_circle_initial_data_folder,
                                                            config.getint('General', 'num_of_json_per_thread'))

    fbc.initiate_osn_dicts_and_sessions(num_of_threads)

    threadList = []
    for i in range(0, num_of_threads):
        threadList.append('Thread-' + str(i))

    i = 0
    threads = []
    for tName in threadList:
        thread = myThread(fbc, i, tName, paths_for_each_thread[i])
        thread.start()
        threads.append(thread)
        i += 1

    for t in threads:
        t.join()
    path_to_csv = fbc.arrange_csv_file_from_mid_data(fbc.json_files_folder, 'data/' + csv_file_name)

    pass
