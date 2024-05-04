import unittest
import sys
import os
sys.path.append('../../')
from andreani_qa_selenium_base.Andreani_QA_Selenium.Selenium import Selenium


class MyTestCase(Selenium, unittest.TestCase):

    def test_000_flujo_basico_pc(self):
        self.flujo_basico()

    def test_001_flujo_basico_server(self):
        self.flujo_basico()

    def test_002_get_enviroment(self):
        os.environ["PYBOT_SYSTEM"] = "server"
        valor_variable = os.getenv("PYBOT_SYSTEM")
        print("El valor de la variable de entorno es:", valor_variable)

    def flujo_basico(self):
        Selenium.json_strings = {
            "<textarea>_1331": {
                "GetFieldBy": "Xpath",
                "ValueToFind": "//textarea[@id=\"APjFqb\"]",
                "Frame": "ROOT"
            }
        }
        Selenium.open_browser(Selenium, "https://www.google.com/", browser='CHROME', privated=False)
        Selenium.get_element(Selenium, "<textarea>_1331").send_keys("testing de prueba")
        Selenium.get_element(Selenium, "<textarea>_1331").send_special_key("ENTER")

    def tearDown(self) -> None:
        Selenium.tear_down(self)


if __name__ == '__main__':
    unittest.main()
