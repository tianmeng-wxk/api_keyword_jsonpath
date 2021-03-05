import unittest,pytest,allure
from ddt import ddt, data, unpack
from common.common import excelData,Convert,depend
from key_word.http import HttpClien
import jsonpath
from log.log import Logger
contents = []
if len(contents) <= 0:
    caseData = excelData().getExcel()
    '''
    {'case1.xlsx': [['http://39.98.138.157:5000/api/login', '{"username":"admin","password":"123456"}', '{"content-type": "application/json"}', 'post', 'json', 'success', '$.msg', 'loginvar'], ['http://39.98.138.157:5000/api/getproductinfo?productid=8888', None, None, 'get', 'url', 200, '$.httpstatus', 'productvar'], ['http://39.98.138.157:5000/api/getuserinfo', None, '{"token": "$loginvar.token$"}', 'get', 'url', 200, '$.httpstatus', 'uservar'], ['http://39.98.138.157:5000/api/addcart', '{"userid":$uservar.data[0].userid$,"openid":"$uservar.data[0].openid$","productid":$productvar.data[0].productid$}', '{"token": "$loginvar.token$","content-type": "application/json"}', 'post', 'json', 200, '$.httpstatus', 'cartinfo'], ['http://39.98.138.157:5000/api/createorder', '{"cartid":$cartinfo.data[0].cartid$,"openid":"$uservar.data[0].openid$","productid":$productvar.data[0].productid$,"userid":$uservar.data[0].userid$}', '{"token": "$loginvar.token$","content-type": "application/json"}', 'post', 'json', 200, '$.httpstatus', '/']],
    'case2.xlsx': [['http://39.98.138.157:5000/api/login', '{"username":"admin","password":"123456"}', '{"content-type": "application/json"}', 'post', 'json', 'success', '$.msg', 'loginvar'], ['http://39.98.138.157:5000/api/getproductinfo?productid=8888', None, None, 'get', 'url', 200, '$.httpstatus', 'productvar'], ['http://39.98.138.157:5000/api/getuserinfo', None, '{"token": "$loginvar.token$"}', 'get', 'url', 200, '$.httpstatus', 'uservar'], ['http://39.98.138.157:5000/api/addcart', '{"userid":$uservar.data[0].userid$,"openid":"$uservar.data[0].openid$","productid":$productvar.data[0].productid$}', '{"token": "$loginvar.token$","content-type": "application/json"}', 'post', 'json', 200, '$.httpstatus', 'cartinfo'], ['http://39.98.138.157:5000/api/createorder', '{"cartid":$cartinfo.data[0].cartid$,"openid":"$uservar.data[0].openid$","productid":$productvar.data[0].productid$,"userid":$uservar.data[0].userid$}', '{"token": "$loginvar.token$","content-type": "application/json"}', 'post', 'json', 200, '$.httpstatus', '/']]}
    '''
    Logger().log().info("测试数据1:{}".format(caseData))
    for name in caseData:
        listCase = caseData[name]
        Logger().log().info("测试数据2:{}".format(listCase))
        for list in listCase:
            contents.append(list)
        Logger().log().info("测试数据3:{}".format(contents))
class TestCase():
    i = 1
    @allure.title("title")
    @pytest.mark.parametrize("url, body, header, method, method_type,expect_value, jsonpath_value, dependency", contents)
    def test_collection(self, url, body, header, method, method_type,expect_value, jsonpath_value, dependency):
        Logger().log().info("开始执行第{}条用例".format(TestCase.i))
        comon=HttpClien()
        body = body.replace('\r', '').replace('\n', '').replace('\t', '') if body is not None else ""
        body = Convert().convert(body) if body.find("$") >= 0 else body


        header = Convert().convert(header) if (header is not None and header.find("$") >= 0) else header
        header = "" if header is None else header
        res=comon.request(method,url,method_type,body,header)
        #把放回数据存入字典depend相应key中
        if len(dependency)>0 and dependency.find("/")<0:
            depend[dependency] = res.content
        res = res.json()
        Logger().log().info("响应结果：{}".format(res))
        jsonpath_value = jsonpath.jsonpath(res,jsonpath_value)
        assert expect_value == jsonpath_value[0],"断言失败"
        TestCase.i = TestCase.i+1