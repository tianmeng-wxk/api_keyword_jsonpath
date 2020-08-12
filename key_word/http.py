import requests
import json


class HttpClien:
    # requests的post请求
    def post(self, url, data=None, headers=None,files=None,**kargs):

        response = requests.post(url=url, data=data, headers=headers, files=files)

        return response

    # requests的get请求
    def get(self, url, params=None, headers=None, **kargs):
        response = requests.get(url=url, params=params, headers=headers)

        return response

    def detelet(self, url, data, headers=None, **kargs):
        response = requests.delete(url=url, data=data, headers=headers)
        return response

    def request(self, requestMethod, requestUrl, paramsType, requestData=None, headers=None, files=None):
        # 判断requestMethod是否是post
        if requestMethod.lower() == "post":
            # paramsType是form表单提交
            if paramsType.lower() == "form":
                response = self.post(url=requestUrl, data=requestData, headers=headers, files=files)
                return response
            # json提交
            elif paramsType == 'json':
                requestData = eval(requestData)
                requestData = json.dumps(requestData)
                headers = eval(headers)
                response = self.post(url=requestUrl, data=requestData, headers=headers, files=files)
                return response

        # 判断requestMethod是否是get
        elif requestMethod == "get":
            if paramsType == "url":

                #request_url = "%s%s" % (requestUrl, "" if requestData is None else  requestData)
                request_url = "{}{}".format(requestUrl, "" if requestData is None else requestData)
                if headers!="":
                    headers=json.loads(headers)
                response = self.get(url=request_url, headers=headers)


                return response
            elif paramsType == "params":
                response = self.get(url=requestUrl, params=requestData, headers=headers)
                return response
