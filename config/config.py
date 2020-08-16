import os
import configparser
import sys
#当前文件所在目录
base_path = os.getcwd()

#用例目录
test_case_path  = '../cases/'

#报告路径
report_path = '../report/'

#发送邮件配置
test_config_file = os.path.join(base_path, '../config', 'config.ini')
rc = configparser.ConfigParser()
rc.read(test_config_file, encoding='utf-8')
host = rc.get('email', 'host')
port = rc.get('email', 'port')
sender = rc.get('email', 'sender')
password = rc.get('email', 'password')
receiver = rc.get('email', 'receiver')