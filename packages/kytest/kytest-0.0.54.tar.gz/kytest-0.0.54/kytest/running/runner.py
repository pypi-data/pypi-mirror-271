import shutil
import pytest

from multiprocessing import Process
from typing import Union, Literal

from kytest.running.conf import App
from kytest.utils.log import logger
from kytest.utils.config import kconfig
from kytest.running.execution_scheduler import (
    _get_case_list,
    _app_main
)


class TestMain(object):
    """
    测试框架入口
    """

    def __init__(
            self,
            proj: str = None,
            path: str = None,
            host: str = None,
            headers: dict = None,
            pkg: str = None,
            did: Union[str, list] = None,
            rule: Union[
                Literal[
                    'full_serial',
                    'full_parallel',
                    'split_serial',
                    'split_parallel'
                ]] = 'full_serial',
            rerun: int = 0,
            xdist: Union[str, int] = False
    ):
        """
        @param proj：测试项目名，跟pytest_util中的project不能重复使用，不然报告会有重复用例
        @param path: 用例路径
        @param host: 域名，用于接口测试和web测试
        @param headers: 请求头，用于接口测试和web测试
        @param pkg:
            安卓包名，通过adb shell pm list packages | grep 'xxx'获取
            IOS包名，通过tidevice applist | grep 'xxx'获取
        @param did:
            安卓设备id： 通过adb devices获取
            IOS设备id：通过tidevice list获取
        @param rule: 多设备执行模式
                - full_serial：每个设备都执行全部用例，串行执行
                - full_parallel：每个设备都执行全部用例，并发执行
                - split_serial：每个设备执行部分用例，串行执行
                - split_parallel：每个设备执行部分用例，并发执行
        @param rerun: 失败重试次数
        @param xdist: 是否并发执行，应该是多进程
        """
        logger.info("kytest start.")
        # 公共参数保存
        # common_data = {
        #     "project": proj,
        #     "base_url": host,
        #     "headers": headers,
        # }
        # kconfig.set_common_dict(common_data)
        kconfig['project'] = proj
        kconfig['base_url'] = host
        kconfig['headers'] = headers

        App.did = did
        App.pkg = pkg

        def _serial_execute(_path):
            # 执行用例
            cmd_list = [
                '-sv',
                '--reruns', str(rerun),
                '--alluredir', 'report', '--clean-alluredir'
            ]

            # if _path is None:
            #     stack_t = inspect.stack()
            #     ins = inspect.getframeinfo(stack_t[1][0])
            #     file_dir = os.path.dirname(os.path.abspath(ins.filename))
            #     file_path = ins.filename
            #     if "\\" in file_path:
            #         this_file = file_path.split("\\")[-1]
            #     elif "/" in file_path:
            #         this_file = file_path.split("/")[-1]
            #     else:
            #         this_file = file_path
            #     _path = os.path.join(file_dir, this_file)

            if _path:
                cmd_list.insert(0, _path)
                if xdist:
                    cmd_list.insert(1, '-n')
                    cmd_list.insert(2, str(xdist))
                    cmd_list.insert(3, '--dist=loadscope')
            else:
                if xdist:
                    cmd_list.insert(0, '-n')
                    cmd_list.insert(1, str(xdist))
                    cmd_list.insert(2, '--dist=loadscope')

            logger.info(cmd_list)
            pytest.main(cmd_list)

        def _parallel_execute(_params):
            if 'parallel' in rule:
                if _params:
                    for param in _params:
                        pr = Process(target=_app_main, args=param)
                        pr.start()
            elif 'serial' in rule:
                if _params:
                    for param in _params:
                        _app_main(*param)

        def _collect_case_and_split(device_id, _path):
            _path_list = [{item: []} for item in device_id]
            test_cases = _get_case_list(_path)
            print(test_cases)
            # 把用例均分成设备数量的份数
            n = len(device_id)
            _lists = [[] for _ in range(n)]
            for _i, item in enumerate(test_cases):
                index = _i % n  # 计算元素应该分配给哪个列表
                _lists[index].append(item)
            return _lists

        # 多设备执行策略
        if isinstance(did, list):
            params = []
            if not did:
                _serial_execute(path)
            elif len(did) == 1:
                App.did = did[0]
                _serial_execute(path)
            else:
                # 清空上次执行的目录
                shutil.rmtree("report", ignore_errors=True)
                if 'full' in rule:
                    for device in did:
                        params.append((path, device, pkg, True))
                else:
                    lists = _collect_case_and_split(did, path)

                    for i in range(len(did)):
                        _path = lists[i][0] if len(lists[1]) < 2 else ','.join(lists[i])
                        params.append((_path, did[i], pkg))

                # 多进程执行
                _parallel_execute(params)

        else:
            _serial_execute(path)

        # 公共参数重置
        kconfig.reset()
        # App参数重置
        App.did = None
        App.pkg = None


main = TestMain

if __name__ == '__main__':
    main()
