import typing

from uiautomator2 import UiObject
from uiautomator2.xpath import XPathSelector

from kytest.adr.driver import Driver
from kytest.utils.exceptions import KError
from kytest.utils.log import logger


class Elem(object):
    """
    安卓元素定义
    """

    def __init__(self,
                 driver: Driver = None,
                 rid: str = None,
                 className: str = None,
                 text: str = None,
                 xpath: str = None,
                 index: int = None,):
        """

        @param driver: 安卓驱动
        @param rid: resourceId定位
        @param className: className定位
        @param text: 文本定位
        @param xpath: xpath定位
        @param index: 识别到多个元素时，根据index获取其中一个
        """
        self._kwargs = {}
        if rid is not None:
            self._kwargs["resourceId"] = rid
        if className is not None:
            self._kwargs["className"] = className
        if text is not None:
            self._kwargs["text"] = text
        if xpath:
            self._kwargs["xpath"] = xpath
        if index is not None:
            self._kwargs["instance"] = index

        self._driver = driver
        self._xpath = xpath

    def __get__(self, instance, owner):
        """po模式中element初始化不需要带driver的关键"""
        if instance is None:
            return None

        self._driver = instance.driver
        return self

    def find(self, timeout=10, watch=None, capture=True):
        """
        增加截图的方法
        @param capture: 是否失败截图
        @param timeout: 每次查找时间
        @param watch: 增加弹窗检测，定位方式列表，用text定位
        watch为True时，使用内置库
            when("继续使用")
            when("移入管控").when("取消")
            when("^立即(下载|更新)").when("取消")
            when("同意")
            when("^(好的|确定)")
            when("继续安装")
            when("安装")
            when("Agree")
            when("ALLOW")
        watch为list时，使用内置库+watch
        @return:
        """

        def _find(is_screen=capture):
            _element = self._driver.d.xpath(self._xpath) if \
                self._xpath is not None else self._driver.d(**self._kwargs)

            if _element.wait(timeout=timeout):
                logger.info(f"查找成功")
                return _element
            else:
                logger.info(f"查找失败")
                if is_screen is True:
                    self._driver.screenshot("查找失败")
                raise KError(f"控件: {self._kwargs}, 查找失败")

        if watch:
            logger.info("开启弹窗检测")
            if isinstance(watch, list):
                with self._driver.d.watch_context(builtin=True) as ctx:
                    for text in watch:
                        ctx.when(text).click()
                    ctx.wait_stable()
                    logger.info("结束检测")
                    return _find()
            else:
                with self._driver.d.watch_context(builtin=True) as ctx:
                    ctx.wait_stable()
                    logger.info("结束检测")
                    return _find()
        else:
            return _find()

    def text(self):
        logger.info(f"获取文本属性")
        _elem = self.find(timeout=3)
        if isinstance(_elem, XPathSelector):
            elems = _elem.all()
        else:
            elems = list(_elem)
        text = []
        for elem in elems:
            text.append(elem.text)

        if len(text) == 1:
            text = text[0]
        logger.info(text)
        return text

    def exists(self, timeout=5):
        logger.info(f"检查控件是否存在")
        result = False
        try:
            _element = self.find(timeout=timeout, capture=False)
            result = True
        except:
            result = False
        finally:
            return result

    @staticmethod
    def _adapt_center(e: typing.Union[UiObject, XPathSelector],
                      offset=(0.5, 0.5)):
        """
        修正控件中心坐标
        """
        if isinstance(e, UiObject):
            return e.center(offset=offset)
        else:
            return e.offset(offset[0], offset[1])

    def click(self, timeout=5, watch=None):
        logger.info(f"点击 {self._kwargs}")
        element = self.find(timeout=timeout, watch=watch)
        x, y = self._adapt_center(element)
        self._driver.util.click(x, y)
        logger.info("点击完成")

    def click_exists(self, timeout=5):
        logger.info(f"{self._kwargs} 存在才点击")
        if self.exists(timeout=timeout):
            self.click(timeout=timeout)
        else:
            logger.info("控件不存在")

    def input(self, text, timeout=5):
        logger.info(f"输入文本: {text}")
        self.click(timeout=timeout)
        self._driver.util.input(text)
        logger.info("输入完成")

    def input_exists(self, text: str, timeout=5):
        logger.info(f"{self._kwargs} 存在才输入: {text}")
        if self.exists(timeout=timeout):
            self.input(text, timeout=timeout)
        else:
            logger.info("输入框不存在")

    def input_pwd(self, text, timeout=5):
        """密码输入框输入有时候用input输入不了"""
        logger.info(f"输入密码: {text}")
        self.click(timeout=timeout)
        self._driver.d(focused=True).set_text(text)
        logger.info("输入完成")

    def assert_exists(self, timeout=3):
        logger.info(f"断言 {self._kwargs} 存在")
        status = self.exists(timeout=timeout)
        assert status, "控件不存在"

    def assert_text(self, text, timeout=3, watch=None):
        logger.info(f"断言 {self._kwargs} 文本属性包括: {text}")
        self.find(timeout=timeout, watch=watch)
        _text = self.text
        assert text in _text, f"文本属性 {_text} 不包含 {text}"


if __name__ == '__main__':
    pass







