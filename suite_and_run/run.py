import pytest,os,time,sys
path = 'E:\\脚本\\api_keywork_jsonpath'
sys.path.append(path)
from common.common import send_email,send_mail

if __name__ == '__main__':
    # pytest.main()
    # #生成pytest-html报告
    # report_path = "../report/"
    # report_file = report_path+"{}_py_html_report.html".format(time.strftime("%Y_%m_%d %H-%M-%S",time.localtime()))
    # if not os.path.exists(report_path):
    #     os.mkdir(report_path)
    # else:
    #     pass
    # pytest.main(["-s", "-v", "../test_case/test_cases.py", "--reruns=5", "--html="+report_file])
    # #-k "关键字" -q 返回简化的控制台 --maxfail=2两次失败就停止 -n=2多线程，命令行中无=  --reruns=5，命令行中无=
    # #--reruns-delay=10命令行中无=
    # send_mail(report_file)

    #生成allure报告
    import os
    pytest.main(['-s','../test_case/test_cases.py', '--alluredir', '../report/html_xml'])#生成alure缓存文件
    os.system('allure generate --clean ../report/html_xml -o ../report/allure_html')
    send_mail('../report/allure_html/index.html')
    # os.system('allure serve ../report/allure_xml')