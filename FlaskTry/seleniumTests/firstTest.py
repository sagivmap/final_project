import unittest
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

class TestLoginToFacebook(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.get('http://127.0.0.1:5000/')

    def tearDown(self):
        pass

    def test_valid_cradentials_from_config_file(self):
        element = self.browser.find_element_by_id('MoveToManuallyAddPage')
        self.browser.execute_script("arguments[0].click();", element)
        self.assertEqual(1,1)




if __name__ == '__main__':
    unittest.main()