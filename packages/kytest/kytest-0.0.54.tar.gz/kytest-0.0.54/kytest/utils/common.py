"""
@Author: kang.yang
@Date: 2023/8/1 18:21
"""
import time
import os
from kytest.utils.log import logger


def general_file_path(file_name):
    logger.info("开始截图")
    if not file_name:
        raise ValueError("文件名不能为空")

    # 截图并保存到当前目录的image文件夹中
    relative_path = "screenshot"
    # 把文件名处理成test.png的样式
    if "." in file_name:
        file_name = file_name.split(r".")[0]
    if os.path.exists(relative_path) is False:
        os.mkdir(relative_path)

    time_str = time.strftime(f"%Y%m%d%H%M%S")
    file_name = f"{time_str}_{file_name}.jpg"
    file_path = os.path.join(relative_path, file_name)
    return file_path




