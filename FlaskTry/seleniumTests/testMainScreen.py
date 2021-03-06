import unittest
from time import sleep
import os
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


class TestAddNewNodes(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.get('http://127.0.0.1:5000/')

    def tearDown(self):
        self.browser.quit()

    # #This test needs a exampleFacebook.csv file in the seleniumTests directory
    def test_upload_csv_facebook(self):
        element = self.browser.find_element_by_id('ChooseFileFacebook')
        self.browser.execute_script("arguments[0].click();", element)
        sleep(5)
        uploadFile = (os.path.dirname(os.path.abspath(__file__)) + "\\files\\exampleFacebook.csv")
        selectFiles = self.browser.find_element_by_id('ChooseFileFacebook').send_keys(uploadFile)
        uploadCSVfile = self.browser.find_element_by_id('uploadCSVFileFacebook')
        self.browser.execute_script("arguments[0].click();", uploadCSVfile)
        sleep(3)
        nodes = self.browser.execute_script("return nodes;")
        links = self.browser.execute_script("return links;")
        self.assertEqual(len(nodes), 6)
        self.assertEqual(len(links), 8)
        self.assertEqual(nodes[0]["id"], "Ego_Node")
        self.assertEqual(nodes[0]["AUA"], '0')
        self.assertEqual(nodes[0]["MF"], '0')
        self.assertEqual(nodes[0]["TF"], '0')
        self.assertEqual(nodes[0]["TSP"], '-1')
        self.assertEqual(nodes[1]["id"], "bob")
        self.assertEqual(nodes[1]["AUA"], '197')
        self.assertEqual(nodes[1]["MF"], '6')
        self.assertEqual(nodes[1]["TF"], '89')
        self.assertEqual(nodes[1]["TSP"], '-1')
        self.assertEqual(nodes[2]["id"], "charlie")
        self.assertEqual(nodes[2]["AUA"], '124')
        self.assertEqual(nodes[2]["MF"], '9')
        self.assertEqual(nodes[2]["TF"], '78')
        self.assertEqual(nodes[2]["TSP"], '-1')
        self.assertEqual(nodes[3]["id"], "david")
        self.assertEqual(nodes[3]["AUA"], '356')
        self.assertEqual(nodes[3]["MF"], '21')
        self.assertEqual(nodes[3]["TF"], '97')
        self.assertEqual(nodes[3]["TSP"], '-1')
        self.assertEqual(nodes[4]["id"], "eve")
        self.assertEqual(nodes[4]["AUA"], '51')
        self.assertEqual(nodes[4]["MF"], '3')
        self.assertEqual(nodes[4]["TF"], '76')
        self.assertEqual(nodes[4]["TSP"], '0.17')
        self.assertEqual(nodes[5]["id"], "frank")
        self.assertEqual(nodes[5]["AUA"], '334')
        self.assertEqual(nodes[5]["MF"], '2')
        self.assertEqual(nodes[5]["TF"], '95')
        self.assertEqual(nodes[5]["TSP"], '0.32')

        self.assertEqual(links[0]["source"]["id"], "Ego_Node")
        self.assertEqual(links[0]["target"]["id"], "bob")
        self.assertEqual(links[1]["source"]["id"], "bob")
        self.assertEqual(links[1]["target"]["id"], "eve")
        self.assertEqual(links[2]["source"]["id"], "Ego_Node")
        self.assertEqual(links[2]["target"]["id"], "david")
        self.assertEqual(links[3]["source"]["id"], "charlie")
        self.assertEqual(links[3]["target"]["id"], "frank")
        self.assertEqual(links[4]["source"]["id"], "david")
        self.assertEqual(links[4]["target"]["id"], "frank")
        self.assertEqual(links[5]["source"]["id"], "Ego_Node")
        self.assertEqual(links[5]["target"]["id"], "charlie")
        self.assertEqual(links[6]["source"]["id"], "david")
        self.assertEqual(links[6]["target"]["id"], "eve")
        self.assertEqual(links[7]["source"]["id"], "charlie")
        self.assertEqual(links[7]["target"]["id"], "eve")


    def test_upload_fail_Facebook(self):
        uploadCSVfile = self.browser.find_element_by_id('uploadCSVFileFacebook')
        self.browser.execute_script("arguments[0].click();", uploadCSVfile)
        sleep(2)
        error = self.browser.find_element_by_id('upload file error')
        self.assertEqual(error.get_attribute('innerHTML').strip(),"No file selected")

if __name__ == '__main__':
    unittest.main()