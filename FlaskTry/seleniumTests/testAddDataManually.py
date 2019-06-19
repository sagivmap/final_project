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
        element = self.browser.find_element_by_id('MoveToManuallyAddPage')
        self.browser.execute_script("arguments[0].click();", element)
        sleep(5)

    def tearDown(self):
        self.browser.quit()

        def test_a(self):
            self.__add_first_circle_node("first", "100", "365", "40", "30", True)

        self.__add_first_circle_node("second", "1", "1", "0", "0", True)
        self.__add_first_circle_node("third", "50", "200", "8", "3", True)
        self.__add_second_circle_node("forth", "1", "1", "2", "0", "0", True)
        self.__add_second_circle_node("forth", "100", "365", "1,3", "40,30", "30,30", True)
        pass

    def test_ego_node(self):
        nodes = self.browser.execute_script("return nodes;")
        self.assertEqual(len(nodes), 1)
        self.assertEqual(nodes[0]['name'], 'Ego Node')
        self.assertEqual(nodes[0]['id'], 0)

    def test_add_first_circle_node_to_graph(self):
        self.browser.find_element_by_id('NodeName').send_keys('OmerSella')
        self.browser.find_element_by_id('TF').send_keys('100')
        self.browser.find_element_by_id('AUA').send_keys('365')
        self.browser.find_element_by_id('CF').send_keys('0')
        self.browser.find_element_by_id('MF').send_keys('40')
        self.browser.find_element_by_id('FD').send_keys('50')
        self.browser.find_element_by_id('AddNodeToGraph').click()
        sleep(2)
        nodes = self.browser.execute_script("return nodes;")
        self.assertEqual(len(nodes), 2)
        self.assertEqual(nodes[1]['name'], 'OmerSella')
        self.assertEqual(nodes[1]['id'], 1)
        self.assertEqual(nodes[1]['AUA'], 365)
        self.assertEqual(len(nodes[1]['CF']), 1)
        self.assertEqual(nodes[1]['CF'][0], 0)
        self.assertEqual(len(nodes[1]['FD']), 1)
        self.assertEqual(nodes[1]['FD'][0], 50)
        self.assertEqual(len(nodes[1]['MF']), 1)
        self.assertEqual(nodes[1]['MF'][0], 40)
        self.assertEqual(nodes[1]['TF'], 100)
        self.assertEqual(nodes[1]["level"], 1)
        self.assertEqual(nodes[1]["TSP"], -1)
        self.assertEqual(nodes[1]["Weight"], 1)

    def test_add_first_circle_node_to_graph_missing_data(self):
        self.assertFalse(self.browser.execute_script("return checkInputValidation();"))
        self.browser.find_element_by_id('NodeName').send_keys('OmerSella')
        self.assertFalse(self.browser.execute_script("return checkInputValidation();"))
        self.browser.find_element_by_id('TF').send_keys('100')
        self.assertFalse(self.browser.execute_script("return checkInputValidation();"))
        self.browser.find_element_by_id('AUA').send_keys('365')
        self.assertFalse(self.browser.execute_script("return checkInputValidation();"))
        self.browser.find_element_by_id('CF').send_keys('0')
        self.assertFalse(self.browser.execute_script("return checkInputValidation();"))
        self.browser.find_element_by_id('MF').send_keys('40')
        self.assertFalse(self.browser.execute_script("return checkInputValidation();"))
        self.browser.find_element_by_id('FD').send_keys('50')
        self.browser.find_element_by_id('AddNodeToGraph').click()
        sleep(1)
        try:
            WebDriverWait(self.browser, 3).until(EC.alert_is_present(),
                                                 'Timed out waiting for PA creation ' +
                                                 'confirmation popup to appear.')
            alert = self.browser.switch_to.alert
            alert.accept()
            self.fail()
        except TimeoutException:
            pass

        self.browser.find_element_by_id('NodeName').clear()
        self.browser.find_element_by_id('NodeName').send_keys('AlexChinyan')
        self.browser.find_element_by_id('MF').clear()
        self.browser.find_element_by_id('MF').send_keys('101')
        self.browser.find_element_by_id('AddNodeToGraph').click()
        sleep(1)
        try:
            WebDriverWait(self.browser, 3).until(EC.alert_is_present(),
                                                 'Timed out waiting for PA creation ' +
                                                 'confirmation popup to appear.')
            alert = self.browser.switch_to.alert
            self.assertEqual(alert.text, 'MF should be less then TF')
            alert.accept()
            self.browser.find_element_by_id('MF').clear()
            self.browser.find_element_by_id('MF').send_keys('90')

            pass
        except TimeoutException:
            self.fail()

        self.browser.find_element_by_id('FD').clear()
        self.browser.find_element_by_id('FD').send_keys('366')
        self.browser.find_element_by_id('AddNodeToGraph').click()
        sleep(1)
        try:
            WebDriverWait(self.browser, 3).until(EC.alert_is_present(),
                                                 'Timed out waiting for PA creation ' +
                                                 'confirmation popup to appear.')
            alert = self.browser.switch_to.alert
            self.assertEqual(alert.text, 'FD should be less then AUA')
            alert.accept()
            self.browser.find_element_by_id('FD').clear()
            self.browser.find_element_by_id('FD').send_keys('200')
            pass
        except TimeoutException:
            self.fail()

        self.browser.find_element_by_id('AddNodeToGraph').click()
        sleep(1)

    def __common_at_adding_nodes(self, name, tf, aua, mf, fd, clear_input):
        self.browser.find_element_by_id('NodeName').send_keys(name)
        self.browser.find_element_by_id('TF').send_keys(tf)
        self.browser.find_element_by_id('AUA').send_keys(aua)
        self.browser.find_element_by_id('MF').send_keys(mf)
        self.browser.find_element_by_id('FD').send_keys(fd)
        self.browser.find_element_by_id('AddNodeToGraph').click()
        sleep(1)
        if clear_input:
            self.__clear_input()

    def __add_first_circle_node(self, name, tf, aua, mf, fd, clear_input):
        self.browser.find_element_by_id('CF').send_keys('0')
        self.__common_at_adding_nodes(name, tf, aua, mf, fd, clear_input)

    def __add_second_circle_node(self, name, tf, aua, cf, mf, fd, clear_input):
        self.browser.find_element_by_id('CF').send_keys(cf)
        self.__common_at_adding_nodes(name, tf, aua, mf, fd, clear_input)

    def __clear_input(self):
        self.browser.find_element_by_id('NodeName').clear()
        self.browser.find_element_by_id('TF').clear()
        self.browser.find_element_by_id('AUA').clear()
        self.browser.find_element_by_id('MF').clear()
        self.browser.find_element_by_id('FD').clear()
        self.browser.find_element_by_id('CF').clear()

    def __get_nodes(self):
        return self.browser.execute_script("return nodes;")

    def __get_links(self):
        return self.browser.execute_script("return links;")

    def __validate_node(self, nodes, id, name, tf, aua, cf, mf, fd, weight, level, tsp):

        for node in nodes:
            if node['id'] == id:
                return (node['name'] == name) and (node['TF'] == tf) and node['AUA'] == aua and node['CF'] == cf \
                       and node['MF'] == mf and node['FD'] == fd and node['Weight'] == weight \
                       and node['level'] == level and node['TSP'] == tsp

        return False

    def __validate_link(self, links, src_id, trg_id, fd, mf, weight):
        for link in links:
            if (link['source']['id'] == src_id and link['target']['id'] == trg_id):
                return link['FD'] == fd and link['MF'] == mf and link['Weight'] == weight

        return False

    def __validate_alert_window(self, msg):
        try:
            WebDriverWait(self.browser, 3).until(EC.alert_is_present(),
                                                 'Timed out waiting for PA creation ' +
                                                 'confirmation popup to appear.')
            alert = self.browser.switch_to.alert
            text = alert.text
            alert.accept()
            self.__clear_input()
            return text == msg
        except TimeoutException:
            return False

    def test_add_second_circle_node(self):
        self.__add_first_circle_node('first', '100', '365', '40', '30', True)
        self.__add_second_circle_node('second', '100', '365', '1', '30', '60', True)
        nodes = self.__get_nodes()
        links = self.__get_links()
        self.assertTrue(self.__validate_node(nodes, 1, 'first', 100, 365, [0], [40], [30], 1, 1, -1))
        self.assertTrue(self.__validate_node(nodes, 2, 'second', 100, 365, [1], [30], [60], 1, 2, 1))
        self.assertTrue(self.__validate_link(links, 0, 1, 30, 40, 1))
        self.assertTrue(self.__validate_link(links, 1, 2, 60, 30, 1))
        pass

    def test_add_second_node_to_not_exits_first_node(self):
        self.__add_second_circle_node('second', '100', '365', '1', '30', '60', False)
        self.assertTrue(self.__validate_alert_window('No such node: 1'))

    def test_add_second_node_with_bad_input_mf_more_tf(self):
        self.__add_first_circle_node('first', '70', '200', '18', '10', True)
        self.__add_second_circle_node('second', '100', '365', '1', '200', '60', False)
        self.assertTrue(self.__validate_alert_window('MF should be less then TF'))
        pass

    def test_add_second_node_with_bad_input_fd_more_aua(self):
        self.__add_first_circle_node('first', '70', '200', '18', '10', True)
        self.__add_second_circle_node('second', '100', '365', '1', '18', '400', False)
        self.assertTrue(self.__validate_alert_window('FD should be less then AUA'))
        pass

    def test_add_second_node_with_bad_input_add_to_egonode_aswell(self):
        self.__add_first_circle_node('first', '70', '200', '18', '10', True)
        self.__add_second_circle_node('second', '100', '365', '0,1', '18,18', '200,200', False)
        self.assertTrue(self.__validate_alert_window('Adding link to Ego node, cannot add to more nodes'))
        pass

    def test_add_second_node_with_bad_input_add_to_partly_exist_first_circle_node(self):
        self.__add_first_circle_node('first', '70', '200', '18', '10', True)
        self.__add_second_circle_node('second', '100', '365', '2,1', '18,18', '200,200', False)
        self.assertTrue(self.__validate_alert_window('No such node: 2'))
        pass

    def test_add_second_node_with_bad_input_add_to_partly_exist_first_circle_node_2(self):
        self.__add_first_circle_node('first', '70', '200', '18', '10', True)
        self.__add_second_circle_node('second', '100', '365', '1,2', '18,18', '200,200', False)
        self.assertTrue(self.__validate_alert_window('No such node: 2'))
        pass

    def test_add_second_node_with_bad_input_add_to_twice_first_node(self):
        self.__add_first_circle_node('first', '70', '200', '18', '10', True)
        self.__add_second_circle_node('second', '100', '365', '1,1', '18,19', '200,201', False)
        self.assertTrue(self.__validate_alert_window('There duplicate CF.'))
        pass

    def test_ego_node(self):
        nodes = self.browser.execute_script("return nodes;")
        self.assertEqual(len(nodes), 1)
        self.assertEqual(nodes[0]['name'], 'Ego Node')
        self.assertEqual(nodes[0]['id'], 0)
        self.assertEqual(nodes[0]['AUA'], "")
        self.assertEqual(len(nodes[0]['CF']), 0)
        self.assertEqual(len(nodes[0]['FD']), 0)
        self.assertEqual(len(nodes[0]['MF']), 0)
        self.assertEqual(nodes[0]['TF'], "")
        self.assertEqual(nodes[0]["level"], 0)
        self.assertEqual(nodes[0]["TSP"], -1)
        self.assertEqual(nodes[0]["Weight"], -1)

    # This test needs a export.json file in the seleniumTests directory
    def test_upload_csv(self):
        uploadFile = (os.path.dirname(os.path.abspath(__file__)) + "\\files\\export.json")
        selectFiles = self.browser.find_element_by_id('selectFiles').send_keys(uploadFile)
        uploadCSVfile = self.browser.find_element_by_id('import')
        self.browser.execute_script("arguments[0].click();", uploadCSVfile)
        sleep(5)
        nodes = self.browser.execute_script("return nodes;")
        self.assertNotEqual(len(nodes), 1)

    def test_download_data(self):
        uploadFile = self.browser.find_element_by_id('DownloadData')
        self.browser.execute_script("arguments[0].click();", uploadFile)
        sleep(5)
        uploadFilePath = (os.path.dirname(os.path.abspath(__file__)) + "\\files\\export.json")
        self.assertEqual(True, os.path.isfile(uploadFilePath));

    def test_TF_checkbox(self):
        checked = self.browser.find_element_by_id(("TFcheckBox")).is_selected()
        TFcheckbox = self.browser.find_element_by_id('TFcheckBox')
        self.browser.execute_script("arguments[0].click();", TFcheckbox)
        isChecked = self.browser.find_element_by_id(("TFcheckBox")).is_selected()
        self.assertEqual(not checked, isChecked)
        sleep(0.5)
        self.browser.execute_script("arguments[0].click();", TFcheckbox)
        isChecked = self.browser.find_element_by_id(("TFcheckBox")).is_selected()
        self.assertEqual(checked, isChecked)

    def test_AUA_checkbox(self):
        checked = self.browser.find_element_by_id(("AUAcheckBox")).is_selected()
        AUAcheckbox = self.browser.find_element_by_id('AUAcheckBox')
        self.browser.execute_script("arguments[0].click();", AUAcheckbox)
        isChecked = self.browser.find_element_by_id(("AUAcheckBox")).is_selected()
        self.assertEqual(not checked, isChecked)
        sleep(0.5)
        self.browser.execute_script("arguments[0].click();", AUAcheckbox)
        isChecked = self.browser.find_element_by_id(("AUAcheckBox")).is_selected()
        self.assertEqual(checked, isChecked)

    def test_MF_checkbox(self):
        checked = self.browser.find_element_by_id(("MFcheckBox")).is_selected()
        MFcheckbox = self.browser.find_element_by_id('MFcheckBox')
        self.browser.execute_script("arguments[0].click();", MFcheckbox)
        isChecked = self.browser.find_element_by_id(("MFcheckBox")).is_selected()
        self.assertEqual(not checked, isChecked)
        sleep(0.5)
        self.browser.execute_script("arguments[0].click();", MFcheckbox)
        isChecked = self.browser.find_element_by_id(("MFcheckBox")).is_selected()
        self.assertEqual(checked, isChecked)

    def test_FD_checkbox(self):
        checked = self.browser.find_element_by_id(("FDcheckBox")).is_selected()
        FDcheckbox = self.browser.find_element_by_id('FDcheckBox')
        self.browser.execute_script("arguments[0].click();", FDcheckbox)
        isChecked = self.browser.find_element_by_id(("FDcheckBox")).is_selected()
        self.assertEqual(not checked, isChecked)
        sleep(0.5)
        self.browser.execute_script("arguments[0].click();", FDcheckbox)
        isChecked = self.browser.find_element_by_id(("FDcheckBox")).is_selected()
        self.assertEqual(checked, isChecked)

    def test_recalculate_TF(self):
        self.__add_first_circle_node('first', '1000', '1', '1', '1', True)
        self.__add_second_circle_node('second', '1000', '1', '1', '1', '1', True)
        sleep(1)
        nodes = self.browser.execute_script("return nodes;")
        self.assertNotEqual(1, nodes[2]["TSP"])
        FDcheckbox = self.browser.find_element_by_id('FDcheckBox')
        self.browser.execute_script("arguments[0].click();", FDcheckbox)
        MFcheckbox = self.browser.find_element_by_id('MFcheckBox')
        self.browser.execute_script("arguments[0].click();", MFcheckbox)
        AUAcheckbox = self.browser.find_element_by_id('AUAcheckBox')
        self.browser.execute_script("arguments[0].click();", AUAcheckbox)
        Recalculatebtn = self.browser.find_element_by_id('Recalculatebtn')
        self.browser.execute_script("arguments[0].click();", Recalculatebtn)
        nodes = self.browser.execute_script("return nodes;")
        self.assertEqual(1, nodes[2]["TSP"])

    def test_recalculate_AUA(self):
        self.__add_first_circle_node('first', '1', '1000', '1', '1', True)
        self.__add_second_circle_node('second', '1', '1000', '1', '1', '1', True)
        sleep(1)
        nodes = self.browser.execute_script("return nodes;")
        self.assertNotEqual(1, nodes[2]["TSP"])
        FDcheckbox = self.browser.find_element_by_id('FDcheckBox')
        self.browser.execute_script("arguments[0].click();", FDcheckbox)
        MFcheckbox = self.browser.find_element_by_id('MFcheckBox')
        self.browser.execute_script("arguments[0].click();", MFcheckbox)
        TFcheckbox = self.browser.find_element_by_id('TFcheckBox')
        self.browser.execute_script("arguments[0].click();", TFcheckbox)
        Recalculatebtn = self.browser.find_element_by_id('Recalculatebtn')
        self.browser.execute_script("arguments[0].click();", Recalculatebtn)
        nodes = self.browser.execute_script("return nodes;")
        self.assertEqual(1, nodes[2]["TSP"])

    def test_recalculate_MF(self):
        self.__add_first_circle_node('first', '1000', '1', '1000', '1', True)
        self.__add_second_circle_node('second', '1000', '1', '1', '1000', '1', True)
        sleep(1)
        nodes = self.browser.execute_script("return nodes;")
        self.assertNotEqual(1, nodes[2]["TSP"])
        FDcheckbox = self.browser.find_element_by_id('FDcheckBox')
        self.browser.execute_script("arguments[0].click();", FDcheckbox)
        AUAcheckbox = self.browser.find_element_by_id('AUAcheckBox')
        self.browser.execute_script("arguments[0].click();", AUAcheckbox)
        TFcheckbox = self.browser.find_element_by_id('TFcheckBox')
        self.browser.execute_script("arguments[0].click();", TFcheckbox)
        Recalculatebtn = self.browser.find_element_by_id('Recalculatebtn')
        self.browser.execute_script("arguments[0].click();", Recalculatebtn)
        nodes = self.browser.execute_script("return nodes;")
        self.assertEqual(1, nodes[2]["TSP"])

    def test_recalculate_FD(self):
        self.__add_first_circle_node('first', '1', '1000', '1', '1000', True)
        self.__add_second_circle_node('second', '1', '1000', '1', '1', '1000', True)
        sleep(1)
        nodes = self.browser.execute_script("return nodes;")
        self.assertNotEqual(1, nodes[2]["TSP"])
        MFcheckbox = self.browser.find_element_by_id('MFcheckBox')
        self.browser.execute_script("arguments[0].click();", MFcheckbox)
        AUAcheckbox = self.browser.find_element_by_id('AUAcheckBox')
        self.browser.execute_script("arguments[0].click();", AUAcheckbox)
        TFcheckbox = self.browser.find_element_by_id('TFcheckBox')
        self.browser.execute_script("arguments[0].click();", TFcheckbox)
        Recalculatebtn = self.browser.find_element_by_id('Recalculatebtn')
        self.browser.execute_script("arguments[0].click();", Recalculatebtn)
        nodes = self.browser.execute_script("return nodes;")
        self.assertEqual(1, nodes[2]["TSP"])

    def test_show_only_bad_connections(self):
        show_only_bad_connections = self.browser.find_element_by_id('show_only_bad_connections')
        self.browser.execute_script("arguments[0].click();", show_only_bad_connections)
        self.assertEqual(self.__validate_alert_window("All connections are GOOD connections!"), True)
        self.__add_first_circle_node('first', '1', '1000', '1', '1000', True)
        self.__add_second_circle_node('second', '1', '1', '1', '1', '1', True)
        show_only_bad_connections = self.browser.find_element_by_id('show_only_bad_connections')
        self.browser.execute_script("arguments[0].click();", show_only_bad_connections)
        self.browser.execute_script("arguments[0].click();", show_only_bad_connections)
        self.assertEqual(self.__validate_alert_window("Already show bad connections.."), True)

    def test_show_all_connections(self):
        Show_All_Connections = self.browser.find_element_by_id('Show All Connections')
        self.browser.execute_script("arguments[0].click();", Show_All_Connections)
        a = self.browser.execute_script("return show_bad_connections;")
        self.assertEqual(a, False)


if __name__ == '__main__':
    unittest.main()