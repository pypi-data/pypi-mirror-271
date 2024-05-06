from kytest import module, title
from kytest.adr import TestCase

from pages.adr_page import DemoPage


@module('测试demo')
class TestAdrDemo(TestCase):

    # def config(self):
    #     self.start_auto = False

    def start(self):
        self.dp = DemoPage(self.driver)

    @title('进入设置页')
    def test_go_setting(self):
        self.dp.adBtn.click_exists()
        self.dp.myTab.click()
        self.dp.setBtn.click()
        self.screenshot("设置页")
        self.sleep(5)



