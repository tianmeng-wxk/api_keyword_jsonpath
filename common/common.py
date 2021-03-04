import openpyxl
import json,jsonpath,os
from log.log import Logger
import smtplib
from email.mime.text import MIMEText#支持html格式
from email.mime.multipart import MIMEMultipart
from email.header import Header
import mysql.connector,zipfile


class excelData:
    def getExcel(self):
        from config.config import test_case_path
        file_name_list = os.walk(test_case_path,topdown=True)
        dict = {}
        for path,dir,file_names in file_name_list:
            try:
                for file_name in file_names:
                    if os.path.splitext(file_name)[1] == '.xlsx':
                        workbook=openpyxl.load_workbook(os.path.join(path,file_name))
                        sheet=workbook["Sheet1"]
                        #定义外层的list结构
                        lists=[]
                        #读取rows
                        row_sheet=sheet.iter_rows()
                        #循环读取每一行，需要赋值每一行为一个list
                        for item in row_sheet:
                            #如果取到第一行就跳出去直接取下一行
                            if item[0].value == "url":
                                continue
                            list=[]
                            for col in item:
                                list.append(col.value)
                            lists.append(list)
                        dict[file_name] = lists
                    else:
                        Logger().log().info("该文件{}非.xlsx后缀".format(file_name))
            except Exception as e:
                Logger().log().error("获取excel数据失败，失败信息：{}".format(e))
        Logger().log().info("dict数据{}".format(dict))
        return dict


depend = {}
class Convert:
    def convert(self,body):
        listsplitvars = body.split("$")
        num = 0
        for listsplitvar in listsplitvars:
            if num % 2 == 1:
                strchuck = listsplitvar
                #环境变量
                envar =strchuck[:strchuck.find(".")]
                varvalue = depend[envar]
                varjsonpath = strchuck[strchuck.find(".")+1:]
                varjsonres = json.loads(varvalue)
                varchuck = jsonpath.jsonpath(varjsonres,expr="$."+varjsonpath)
                listsplitvars[num]=str(varchuck[0])
            num += 1
        listsplitvars = "".join(listsplitvars)

        return listsplitvars

#发送附件邮件
def send_email(email_path):
    message = MIMEMultipart()
    #邮件内容
    text = """
    请输入你想说的邮件内容
    """
    message.attach(MIMEText(_text=text, _subtype='plain', _charset="utf-8"))
    #需要发送的附件的路径
    with open(email_path, 'rb') as f:
        content = f.read()
    att1 = MIMEText(content, "base64", "utf-8")
    att1["Content-Type"] = 'application/octet-stream'
    att1['Content-Disposition'] = 'attachment; filename = "report.html"'
    message.attach(att1)

    #邮件主题
    message["Subject"] = Header("主题", "utf-8").encode()
    message["From"] = Header("tianmeng", "utf-8")
    message["To"] = Header('tianmeng_wxk', "utf-8")

    try:
        smtp = smtplib.SMTP()
        #smtp = smtplib.SMTP_SSL('smtp.163.com', 465)
        smtp.connect(host="smtp.qq.com", port=587)
        smtp.login(user="3394788013@qq.com", password="lizceyidpekpdbhd")
        sender = "3394788013@qq.com"
        receiver = ['tianmeng_wxk@163.com']
        smtp.sendmail(sender, receiver, message.as_string())
        Logger().log().info("发送邮件成功")
        return email_path
    except smtplib.SMTPException as e:
        Logger().log().info("发送邮件失败，失败信息：{}".format(e))

#发送html格式邮件（需要修改报告源码）
def send_mail(email_path):
    from config.config import host, port, password, sender, receiver
    with open(email_path, 'rb') as f:
        content = f.read()
    host = host
    port = port
    sender = sender
    password = password
    receiver = receiver
    message = MIMEText(content, "HTML", "UTF-8")
    message["Subject"] = "接口测试"
    message["From"] = sender
    message["To"] = receiver
    try:
        smtp = smtplib.SMTP(host, port)
        smtp.login(sender,password)
        smtp.sendmail(sender, receiver, message.as_string())
        Logger().log().info("发送邮件成功")
    except smtplib.SMTPException as e:
        Logger().log().info("发送邮件失败，失败信息：{}".format(e))


def connect_mysql(sql):
    ccon=mysql.connector.connect(
        host='localhost',
        user='root',
        password='wxk111',
        database='first'
    )
    print(ccon)
    cmd=ccon.cursor()
    # cmd.execute("show databases;")
    # for x in cmd:
    #     print(x)
    cmd.execute("{}".format(sql))
    res=cmd.fetchall()
    return res[0][0]

def get_sql_data(sql):
    sql = connect_mysql(sql)
    return sql


def link_oracle():
    import cx_Oracle
    #conn = cx_Oracle.connect('name/password@ip:port/serverName')      # 连接数据库
    conn = cx_Oracle.connect('cwhs/cwhs@192.168.1.201:1521/helowin')
    c = conn.cursor()                                                 # 获取cursor
    x = c.execute("select * from ZZ_KMZZ")                            # 查询
    print("result: ", x.fetchone())
    c.close()                                                         # 关闭cursor
    conn.close()
#压缩
def zipDir(dirpath,outFullName):
    """
    压缩指定文件夹
    :param dirpath: 目标文件夹路径
    :param outFullName: 压缩文件保存路径+xxxx.zip
    :return: 无
    """
    zip = zipfile.ZipFile(outFullName,"w",zipfile.ZIP_DEFLATED)
    for path,dirnames,filenames in os.walk(dirpath):
        # 去掉目标跟路径，只对目标文件夹下边的文件及文件夹进行压缩
        fpath = path.replace(dirpath,'')

        for filename in filenames:
            zip.write(os.path.join(path,filename),os.path.join(fpath,filename))
    zip.close()
#解压
def decompression():
    zip_file = zipfile.ZipFile("D:/WebContent/assist_web.zip")
    zip_list = zip_file.namelist()
    for f in zip_list:
        zip_file.extract(f, "D:/WebContent/assist_web")  # 循环解压文件到指定目录
    zip_file.close()
#md5加密
def hashmd5(str):
    import hashlib
    return hashlib.md5(str.encode('utf-8')).hexdigest()

if __name__ == '__main__':
    link_oracle()

# import cx_Oracle as oracle
# from readConfig import get_config_values
# from utils.resutltodict import dict_fetchall
#
#
# def execute_oracle_sql_query(sql, params):
#     """
#     执行oracle sql查询语句
#     :param sql: sql语句，变量使用 :var或者:1,:2表示
#     :param params: 变量值，传入元祖
#     :return: queryset
#     """
#     dsn_tns = oracle.makedsn(get_config_values('oracle', 'host'), get_config_values('oracle', 'port'),
#                              get_config_values('oracle', 'sid'))
#     print(dsn_tns)
#     conn = oracle.connect(user=get_config_values('oracle', 'user'), password=get_config_values('oracle', 'password'),
#                           dsn=dsn_tns)
#     cursor = conn.cursor()
#     cursor.execute(sql, params)
#     qryset = dict_fetchall(cursor)
#     cursor.close()
#     conn.close()
#     return qryset
#
# if __name__ == '__main__':
#     sql = """select t.*,rowid from ch_info_dictitem t where t.groupid=:1"""
#     params = ('WorkFlowCategory', )
#     print(execute_oracle_sql_query(sql=sql, params=params