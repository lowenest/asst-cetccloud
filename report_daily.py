# -*- coding: utf-8 -*-

import urllib.request
import gzip
import json
import datetime
import time
import ast
import ssl

def ungzip(data):
    try:
        data = gzip.decompress(data)
    except:
        pass
    return data


# ms
def composeTime(time1):
    time2 = datetime.datetime.strptime(time1, "%Y-%m-%d %H:%M:%S")
    time3 = time.mktime(time2.timetuple())
    time4 = int(time3)
    return time4

if __name__ == '__main__':

    # 构建一个已经登录过的用户的headers信息
    headers = {
        "Host": "asst.cetccloud.com",
        "requestType": "zuul",
        "accessToken": "null",
        "DNT": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36",
        "applyID": "df626fdc9ad84d3a95633c10124df358",
        "Content-Type": "multipart/form-data; boundary=----WebKitFormBoundarynRRv3uNvLvoCVVw1",
        "Cookie": "SESSION=MGMzNWI3MzgtZmVlZC00YWEzLWIwOTUtMjJhNjliOTU2OGNh",
        "secretKey": "D8FE427008F065C1B781917E82E1EC1E",
        "Origin": "https://asst.cetccloud.com",
        "Referer": "https://asst.cetccloud.com/",
        "Accept-Language": "en,zh-CN;q=0.9,zh;q=0.8,en-US;q=0.7,zh-TW;q=0.6"
    }

    loginFormData = {
        "mobile": "15888888888",
        "password": "123456",
        "client": "h5"
    }
    data = urllib.parse.urlencode(loginFormData).encode("UTF-8");

    ssl._create_default_https_context = ssl._create_unverified_context
    # 通过headers里的报头信息（主要是Cookie信息），构建Request对象
    request = urllib.request.Request(
        url="https://asst.cetccloud.com/ncov/login?mobile=15888888888&password=123456&client=h5", data=data, headers=headers,
        method="POST")

    response = urllib.request.urlopen(request)

    # 打印响应内容
    decodeResponse = ungzip(response).read().decode("UTF-8")
    # print (decodeResponse)

    jsonResp = json.loads(decodeResponse)
    accessToken = jsonResp["data"]["userInfo"]["accessToken"]
    # print(accessToken)

    urlDailyReport = "https://asst.cetccloud.com/oort/oortcloud-2019-ncov-report/2019-nCov/report/everyday_report"
    requestDailyReport = urllib.request.Request(url=urlDailyReport, data=data, headers=headers, method="POST")
    requestDailyReport.add_header("accessToken", "bb92a877d5574890a0adc2902d97b466")
    requestDailyReport.add_header("Content-Type", "application/json")
    requestDailyReport.add_header("Accept", "application/json")


    today = time.strftime("%Y-%m-%d", time.localtime(time.time()))
    startTs = str(composeTime(today + " 08:30:00")) + "000"
    endTs = str(composeTime(today + " 20:00:00")) + "000"

    mya= r'{"phone":"15888888888","Traffic_data":{"bike":0,"bike_way":"","bus":0,"bus_number":"","car":0,"car_way":"","metro":0,"metro_number":"","other":0,"other_way":"","walk":0,"walk_way":"","phone":"15888888888"},"physical_data":{"type1":0,"type1_state":"0","type2":0,"type3":0,"type4":0,"type5":0,"type6":0,"type7":0,"type7_state":"","phone":"15888888888"},"track_data":{"tracks":"[{\"area\":\"地址@#\",\"start\":\"'+startTs+r'\",\"end\":\"'+endTs+r'\"}]","phone":"15888888888"},"work_way":0,"touch":0,"accessToken":"'+accessToken+'"}'

    dataDailyReport = ast.literal_eval(mya)
    reportBytes= bytes(mya,"UTF-8")

    responseDailyReport = urllib.request.urlopen(requestDailyReport, data=reportBytes)
    decodeResponseDailyReport = ungzip(responseDailyReport).read().decode("UTF-8")

    print(decodeResponseDailyReport)
