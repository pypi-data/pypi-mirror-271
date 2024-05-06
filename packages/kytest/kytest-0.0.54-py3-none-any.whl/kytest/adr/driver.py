import allure
import uiautomator2 as u2

from kytest.utils.log import logger
from kytest.adr.utils import Util
from kytest.utils.common import general_file_path


class Driver:

    def __init__(self, device_id=None):
        if device_id:
            self.device_id = device_id
        else:
            self.device_id = Util.get_first_device()
        logger.info(f"初始化安卓驱动: {device_id}")

        self.d = u2.connect(self.device_id)
        self.util = Util(self.device_id)

    # def uninstall_app(self, pkg_name=None):
    #     logger.info(f"卸载应用")
    #     if pkg_name is not None:
    #         self.pkg_name = pkg_name
    #     if self.pkg_name is None:
    #         raise KeyError("应用包名不能为空")
    #     self.d.app_uninstall(self.pkg_name)
    #
    # @staticmethod
    # def download_apk(src):
    #     """下载安装包"""
    #     start = time.time()
    #     if isinstance(src, six.string_types):
    #         if re.match(r"^https?://", src):
    #             logger.info(f'下载中...')
    #             file_path = os.path.join(os.getcwd(), src.split('/')[-1])
    #             r = requests.get(src, stream=True)
    #             if r.status_code != 200:
    #                 raise IOError(
    #                     "Request URL {!r} status_code {}".format(src, r.status_code))
    #             with open(file_path, 'wb') as f:
    #                 f.write(r.content)
    #             end = time.time()
    #             logger.info(f'下载成功: {file_path}，耗时: {end - start}s')
    #             return file_path
    #         elif os.path.isfile(src):
    #             return src
    #         else:
    #             raise IOError("static {!r} not found".format(src))
    #
    # def install_app(self, apk_path, auth=True, new=True, helper: list = None, pkg_name=None):
    #     """
    #     安装应用，push改成adb命令之后暂时无法支持远程手机调用
    #     @param pkg_name:
    #     @param apk_path: 安装包链接，支持本地路径以及http路径
    #     @param auth: 是否进行授权
    #     @param new: 是否先卸载再安装
    #     @param helper：install命令后的各品牌机型适配
    #     [
    #         ["assert", {"text": "未发现风险"}],
    #         ["click", {"text": "继续安装"}],
    #         ["click", {"text": "完成"}],
    #         ["input", {"resourceId": "xxx"}, "yyy"]
    #     ]
    #     """
    #     start = time.time()
    #     logger.info(f"安装应用: {apk_path}")
    #     # 卸载
    #     if new is True:
    #         if pkg_name is not None:
    #             self.pkg_name = pkg_name
    #         if self.pkg_name is None:
    #             raise KeyError("应用包名不能为空")
    #         self.uninstall_app()
    #
    #     # 下载
    #     try:
    #         source = self.download_apk(apk_path)
    #     except:
    #         raise KeyError("下载apk失败")
    #
    #     # 安装
    #     try:
    #         cmd_list = ['adb', 'install', "-r", "-t", source]
    #         if auth is True:
    #             cmd_list.insert(4, '-g')
    #         logger.debug(f"{' '.join(cmd_list)}")
    #         process = subprocess.Popen(cmd_list,
    #                                    stdout=subprocess.PIPE,
    #                                    stderr=subprocess.PIPE)
    #         if helper is None:
    #             # 等待子进程执行完成
    #             process.wait()
    #     except:
    #         raise KeyError("adb安装失败")
    #
    #     # 各品牌机型适配
    #     try:
    #         if helper is not None:
    #             for step in helper:
    #                 method = step[0]
    #                 loc = step[1]
    #                 if method == "click":
    #                     self.d(**loc).click()
    #                 elif method == "assert":
    #                     assert self.d(**loc).wait(timeout=10)
    #                 elif method == "input":
    #                     content = step[2]
    #                     self.d(**loc).send_keys(content)
    #                 else:
    #                     raise KeyError("不支持的方法")
    #     except:
    #         raise KeyError("安装过程处理失败")
    #
    #     # 删除下载的安装包
    #     if 'http' in apk_path:
    #         os.remove(source)
    #
    #     end = time.time()
    #     logger.info(f'安装成功，耗时: {end - start}s')

    def screenshot(self, file_name=None):
        file_path = general_file_path(file_name)
        logger.info(f"截图保存至: {file_path}")
        self.d.screenshot(file_path)

        logger.info("截图上传allure报告")
        allure.attach.file(
            file_path,
            attachment_type=allure.attachment_type.PNG,
            name=f"{file_path}",
        )
        return file_path


if __name__ == '__main__':
    pass















