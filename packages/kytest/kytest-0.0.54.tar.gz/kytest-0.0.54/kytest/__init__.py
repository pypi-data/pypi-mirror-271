from .case import TestCase
from .page import Page
from .running.runner import main
from .running.conf import App
from .utils.config import kconfig
from .utils.pytest_util import *
from .utils.allure_util import *
from .utils.log import logger
from .utils.exceptions import KError

__version__ = "0.0.54"
__description__ = "API/安卓/IOS/WEB平台自动化测试框架"
