import pytest,os,time,sys
path = 'E:\\script\\api_keywork_jsonpath'
sys.path.append(path)

if __name__ == '__main__':
    # pytest.main()
    # #生成pytest-html报告
    # report_path = "../report/"
    # report_file = report_path+"{}_py_html_report.html".format(time.strftime("%Y_%m_%d %H-%M-%S",time.localtime()))
    # if not os.path.exists(report_path):
    #     os.mkdir(report_path)
    # else:
    #     pass
    # pytest.main(["-s", "-v", "../test_case/test_cases.py",'--self-contained-html',"--reruns=5", "--html="+report_file])
    # #-k "关键字" -q 返回简化的控制台 --maxfail=2两次失败就停止 -n=2多线程，命令行中无=  失败的重新运行5遍--reruns=5，命令行中无=
    # #添加重运行等待时间--reruns-delay=10命令行中无=
    #--lf 只运行上一次失败的用例，--ff先运行上一次失败的用例再运行成功的用例
    # send_mail(report_file)

    #生成allure报告
    import os
    pytest.main(['-s', '../test_case/test_cases.py', '--alluredir', '../report/allure-results'])#生成alure缓存文件
    os.system('allure generate ../report/allure-results -o ../report/allure-report --clean')
    # zipDir("../../api_keywork_jsonpath","../file/zip.zip")
    # SendEmail().send_email('../file/zip.zip')
    # os.system('allure serve ../report/allure_xml')
    #import subprocess
    #subprocess.run('allure serve ../report/allure_xml',shell=True)