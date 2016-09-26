# -*- coding: UTF-8 -*-
import urllib
import httplib
import config
import time

LOG_FILE = "xk.log"

ERROR_CONFIGURATION = "Invalid Configuration\n"

fLog = open(LOG_FILE, "a")

if (len(config.CLASS_NO) != len(config.COURSE_CODE)):
    print ERROR_CONFIGURATION
    fLog.write(ERROR_CONFIGURATION)
    fLog.close()
    exit(0)

path = "/xsxk/elect.xk"
headers = {
    "Host": "xkfw.xjtu.edu.cn",
    "User-Agent": config.UA,
    "Cookie": config.COOKIE,
    "Referer": "http://xkfw.xjtu.edu.cn/xsxk/jctslkc.xk",
}
paramsStr = {
    "method": "handleZxxk",
    "jxbid": "",
    "xklx": 3,
    "xkzy": 3,
    "ysJxbid": ""
}
conn = httplib.HTTPConnection(headers["Host"])
capacity = len(config.COURSE_CODE)
selected = [False]*capacity
while True:
    if not (False in selected):
        break
    for i in range(capacity):
        if not selected[i]:
            paramsStr["jxbid"] = "%d%s00-%s" % (config.TERM, config.COURSE_CODE[i], config.CLASS_NO[i])
            params = urllib.urlencode(paramsStr)
            conn.request(method="GET", url="%s?%s"%(path, params), headers=headers)
            response = conn.getresponse()
            content = response.read()
            log = "[%s] %s %s %s %s\n" % (time.strftime("%Y-%m-%d %H:%M:%S"), config.COURSE_CODE[i], response.status, response.reason, content)
            print log
            fLog.write(log)
            fLog.flush()
            if response.status == 200:
                for cond in config.STOP_CONDITION:
                    if cond in content:
                        selected[i] = True
                        break
            time.sleep(config.INTERVAL)
fLog.close()