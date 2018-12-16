from datetime import datetime
from time import sleep
import monthdelta
import os
import csv
import json
import re

class utils:
    def __init__(self, logger):
        self.logger = logger

    def get_timestamp(self):
        return str(datetime.now().strftime('%Y_%m_%d_%H_%M_%S'))

    def write_row_in_csv_file(self, path_to_file, row):
        with open(path_to_file, 'w', newline='') as csvFile:
            writer = csv.writer(csvFile)
            writer.writerow(row)

        csvFile.close()

    def write_rows_in_csv_file(self, path_to_file, rows):
        with open(path_to_file, 'a', newline='') as csvFile:
            writer = csv.writer(csvFile)
            writer.writerows(rows)

        csvFile.close()

    def append_row_in_csv_file(self, file, row):
        with open('data/'+file, 'a') as csvFile:
            writer = csv.writer(csvFile)
            writer.writerow(row)

        csvFile.close()

    def customized_get_request(self, url, session, cookies, num_of_attempts):
        succeed_to_get = False
        for j in range(num_of_attempts):
            r = session.get(url,cookies=cookies, allow_redirects=False)
            if r.status_code == 200:
                succeed_to_get = True
                return succeed_to_get, r

            elif j < num_of_attempts - 1:
                self.logger.error('Got ' + str(r.status_code) + ' instead of 200,' + '\nFor url: ' + url)
                sleep(10)
        return succeed_to_get, r

    def customized_redirected_get_request(self, url, session, cookies, num_of_attempts):
        succeed_to_get = False
        for j in range(num_of_attempts):
            r = session.get(url,cookies=cookies, allow_redirects=False)
            if r.status_code == 302 and hasattr(r, '_next'):
                r = session.get(r._next.url, cookies=cookies, allow_redirects=False)
                if r.status_code == 200:
                    succeed_to_get = True
                    return succeed_to_get, r

                elif j < num_of_attempts - 1:
                    self.logger.error('Got ' + str(r.status_code) + ' instead of 200,' + '\nFor url: ' + url)
                    sleep(10)

            elif j < num_of_attempts - 1:
                self.logger.error('Got ' + str(r.status_code) + ' instead of 302, ' + '\nFor url: ' + url)
                sleep(10)
        return succeed_to_get, r

    def save_to_json_file(self, data, path):
        path = path + '_' + self.get_timestamp() + '.json'
        with open(path, 'w') as outfile:
            json.dump(data, outfile, indent=4)

    def save_to_json_file_no_TS(self, data, path):
        path = path + '.json'
        with open(path, 'w') as outfile:
            json.dump(data, outfile, indent=4)

    def make_dir(self, dir_path):
        os.makedirs(dir_path)

    def load_json_file(self, path_to_json_file):
        with open(path_to_json_file) as f:
            data = json.load(f)

        return data


    def convert_friendship_duration_text_to_month(self, month_year):
        start = datetime.strptime(month_year, "%B %Y")
        today = datetime.now()
        return monthdelta.monthmod(start, today)[0].months

    def convert_only_month_friendship_duration_text_to_month(self, month):
        start = datetime.strptime(month + ' ' + str(datetime.now().year) , "%B %Y")
        today = datetime.now()
        return monthdelta.monthmod(start, today)[0].months

    def get_num_of_days_from_first_post_date(self, date_text):
        if re.search(r'^(\w{3,9} \d{1,2}\, \d{4})', date_text):
            start = datetime.strptime(re.search(r'^(\w{3,9} \d{1,2}\, \d{4})', date_text).group(1), "%B %d, %Y")
        elif re.search(r'^(\w{3,9} \d{1,2})', date_text):
            start = datetime.strptime(re.search(r'^(\w{3,9} \d{1,2})', date_text).group(1) +  ' ' + str(datetime.now().year), "%B %d %Y")
        else:
            return None
        today = datetime.now()
        return  abs((start - today).days)

    def get_amount_of_friends_from_text(self, friend_amount_text):
        ans = re.match(r'Friends \((\d+)\)', friend_amount_text)
        if ans:
            return int(ans.group(1))

        ans = re.match(r'Friends \((\d+\,\d+)\)', friend_amount_text)
        if ans:
            return int(ans.group(1).replace(',',''))

    def get_sc_id_from_uri(self, uri):
        if uri.startswith('/profile.php'):
            return re.split(r'\/|\?|\&|\=',uri)[3]
        return re.split(r'\/|\?',uri)[1]

    def get_fc_id_from_uri(self, uri):
        if uri.startswith('/profile.php'):
            return re.split(r'\/|\?|\&|\=',uri)[7]
        return re.split(r'\/|\?',uri)[1]

    def get_mutual_friend_from_text(self, text):
        ans = re.match(r'(\d+) mutual friend(s){0,1}', text)
        if ans:
            return int(ans.group(1))

    def get_days_since_start_of_year(self, year):
        start = datetime.strptime(year, "%Y")
        today = datetime.now()
        return abs((start - today).days)

    def get_paths_for_each_thread(self, path_to_jsons_folder, num_of_json_per_thread):
        json_files = [os.path.join(path_to_jsons_folder,f) for f in os.listdir(path_to_jsons_folder) if os.path.isfile(os.path.join(path_to_jsons_folder, f))]
        json_files = sorted(json_files, key=len)
        return [json_files[i:i+num_of_json_per_thread] for i in range(0,len(json_files),num_of_json_per_thread)]

    def get_all_json_files_in_path(self, path_to_folder):
        return [f for f in os.listdir(path_to_folder) if os.path.isfile(os.path.join(path_to_folder, f))]