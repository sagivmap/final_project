import unittest
from time import sleep

from selenium import webdriver
import os

class TestAddNewNodes(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.get('http://127.0.0.1:5000/')

    def tearDown(self):
        pass

    def test_ego_node(self):
        element = self.browser.find_element_by_id('MoveToManuallyAddPage')
        self.browser.execute_script("arguments[0].click();", element)
        sleep(5)
        nodes = self.browser.execute_script("return nodes;")
        self.assertEqual(len(nodes),1)
        self.assertEqual(nodes[0]['name'], 'Ego Node')
        self.assertEqual(nodes[0]['id'], 0)
        self.assertEqual(nodes[0]['AUA'], "")
        self.assertEqual(len(nodes[0]['CF']),0)
        self.assertEqual(len(nodes[0]['FD']),0)
        self.assertEqual(len(nodes[0]['MF']),0)
        self.assertEqual(nodes[0]['TF'], "")
        self.assertEqual(nodes[0]["level"],0)
        self.assertEqual(nodes[0]["TSP"],-1)
        self.assertEqual(nodes[0]["Weight"],-1)

    #This test needs a export.json file in the seleniumTests directory
    def test_upload_csv(self):
        element = self.browser.find_element_by_id('MoveToManuallyAddPage')
        self.browser.execute_script("arguments[0].click();", element)
        sleep(5)
        uploadFile=(os.path.dirname(os.path.abspath(__file__))+"\\files\\export.json")
        selectFiles=self.browser.find_element_by_id('selectFiles').send_keys(uploadFile)
        uploadCSVfile=self.browser.find_element_by_id('import')
        self.browser.execute_script("arguments[0].click();", uploadCSVfile)
        sleep(5)
        nodes = self.browser.execute_script("return nodes;")
        self.assertNotEqual(len(nodes),1)

if __name__ == '__main__':
    unittest.main()