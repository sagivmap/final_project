import unittest
from datetime import datetime
from bs4 import BeautifulSoup
from Crawler.FBCrawler import FBCrawler

fbc = FBCrawler("test_data")
COOKIES = None
SESSION = None
class TestLoginToFacebook(unittest.TestCase):

    def test_valid_cradentials_from_config_file(self):
        COOKIES, SESSION = fbc.login_to_facebook()
        self.assertIsNotNone(COOKIES)
        self.assertIsNotNone(SESSION)
        fbc.session_and_cookies.append((SESSION,COOKIES))

    def test_non_valid_pass_from_config_file(self):
        session_cookies, session = fbc.login_to_facebook(password="NONVALIDPASS")
        self.assertEqual(session_cookies, None)
        self.assertEqual(session, None)

    def test_non_valid_email_from_config_file(self):
        session_cookies, session = fbc.login_to_facebook(email="NONVALIDMAIL@gmail.com")
        self.assertEqual(session_cookies, None)
        self.assertEqual(session, None)

class TestFriendshipDuration(unittest.TestCase):

    def test_friendship_duration_month_and_year(self):
        soup = BeautifulSoup(open("html_pages_to_test/friendship_duration_page_month_and_year.html", encoding="utf8"),
                             features="html.parser")
        friendship_in_months = fbc._get_friendship_duration_as_months(soup)
        now = datetime.today()
        friend_since = datetime(2017,8,1)
        expected_month = (now.year - friend_since.year) * 12 + now.month - friend_since.month
        self.assertEqual(expected_month, friendship_in_months)

    def test_not_available_friendship_duration(self):
        soup = BeautifulSoup(open("html_pages_to_test/friendship_duration_not_available.html", encoding="utf8"),
                             features="html.parser")
        friendship_in_months = fbc._get_friendship_duration_as_months(soup)
        self.assertIsNone(friendship_in_months)


class TestFacebookUserAge(unittest.TestCase):

    def test_facebook_user_age_with_first_post(self):
        now = datetime.now()
        start = datetime.strptime("December 17, 2009", "%B %d, %Y")
        expected = abs((start - now).days)
        COOKIES, SESSION = fbc.login_to_facebook()
        fbc.session_and_cookies[0] = (SESSION, COOKIES)
        soup = BeautifulSoup(open("html_pages_to_test/facebook_user_age_with_last_post.html", encoding="utf8"),
                             features="html.parser")
        days_age = fbc._get_FB_user_account_age_as_days(soup, 0)
        self.assertEqual(expected, days_age)
        SESSION.close()


class TestAmountOfFriends(unittest.TestCase):

    def test_fb_user_amount_of_friends(self):
        uri_to_friend_list = "/abel.andsimien/friends"
        COOKIES, SESSION = fbc.login_to_facebook()
        if len(fbc.session_and_cookies) == 0:
            fbc.session_and_cookies.append((SESSION, COOKIES))
        else:
            fbc.session_and_cookies[0] = (SESSION, COOKIES)
        amount_of_friends = fbc._get_facebook_user_amount_of_friends(uri_to_friend_list, 0)
        self.assertEqual(97, amount_of_friends[0])
        SESSION.close()

    def test_fb_user_no_amount_available(self):
        uri_to_friend_list = "/skileta/friends"
        COOKIES, SESSION = fbc.login_to_facebook()
        if len(fbc.session_and_cookies) == 0:
            fbc.session_and_cookies.append((SESSION, COOKIES))
        else:
            fbc.session_and_cookies[0] = (SESSION, COOKIES)
        amount_of_friends = fbc._get_facebook_user_amount_of_friends(uri_to_friend_list, 0)
        self.assertEqual(None, amount_of_friends[0])
        SESSION.close()


if __name__ == '__main__':
    test_classes_to_run = [TestLoginToFacebook,
                           TestFriendshipDuration,
                           TestFacebookUserAge,
                           TestAmountOfFriends]

    loader = unittest.TestLoader()

    suites_list = []
    for test_class in test_classes_to_run:
        suite = loader.loadTestsFromTestCase(test_class)
        suites_list.append(suite)

    big_suite = unittest.TestSuite(suites_list)

    runner = unittest.TextTestRunner()
    results = runner.run(big_suite)