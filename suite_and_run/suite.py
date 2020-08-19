#coding=utf-8
import unittest,os,sys,time
path = "../"
sys.path.append(path)
from HTMLTestRunner import HTMLTestRunner
from test_case.test_cases import TestCase
from datetime import datetime
from common.common import send_mail,send_email,Logger



# path = curPath+"../../test_case"
# discover = unittest.defaultTestLoader.discover(start_dir=path, pattern="read_*.py")#在path目录下运行以read开头的文件,运行discover

def suite():
    from config.config import report_path
    suite = unittest.TestSuite()
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestCase))
    report_path = report_path
    report_file = report_path+"{}_html_report.html".format(time.strftime("%Y-%m-%d %H-%M-%S",time.localtime()))
    # time = datetime.now()
    # now = time.strftime('%Y-%m-%d %H-%M-%S')
    # report_file = report_path + now + "_html_report.html"
    if not os.path.exists(report_path):
        os.mkdir(report_path)
    else:
        pass

    with open(report_file, 'wb')as file:
        runner = HTMLTestRunner(stream=file, verbosity=2, title="接口测试", description="接口测试")
        runner.run(suite)

    send_mail(report_file)
if __name__ == '__main__':
    suite()