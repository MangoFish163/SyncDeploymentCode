# logger.py

import logging
import os
from mainConfig import LOGFILE

def logger_file_size(file_path):
    try:
        # 获取文件大小，单位为字节
        size = os.path.getsize(file_path)
        return size
    except OSError as e:
        # 如果文件不存在或者其他错误，返回错误信息
        print(f"Error: {e}")
        return None

def logger_rename_and_backup(file_path, backup_path, max_size=10 * 1024 * 1024):
    size = logger_file_size(file_path)
    if size is not None and size > max_size:
        try:
            # 如果备份文件已经存在，先删除它
            if os.path.exists(backup_path):
                os.remove(backup_path)
            # 重命名文件
            os.rename(file_path, backup_path)
        except OSError as e:
            print(f"Error during renaming: {e}")
def get_logger(name='default'):
    if not os.path.exists('logs'):
        os.makedirs('logs')
    logger = logging.getLogger(name)
    if not logger.hasHandlers():
        logger.setLevel(logging.INFO)
        if name == 'default' and os.path.exists('logs/'+LOGFILE):
            logger_rename_and_backup('logs/'+LOGFILE, 'logs/app-backup.log')
        elif name == 'webhook' and os.path.exists('logs/webhook.log'):
            logger_rename_and_backup('logs/webhook.log', 'logs/webhook-backup.log')
        elif os.path.exists(f'logs/{name}.log'):
            logger_rename_and_backup(f'logs/{name}.log', f'logs/{name}.log')
        # 创建一个FileHandler，用于将日志写入文件
        file_handler = logging.FileHandler(f'logs/{name}.log',encoding='utf-8')
        file_handler.setLevel(logging.INFO)

        # 创建一个Formatter，用于设置日志输出格式
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)

        # 将FileHandler添加到Logger对象中
        logger.addHandler(file_handler)
    return logger
