# 发送一个接口请求，返回成功次数、响应时间等，这个脚本针对请求参数中deviceid需要每次请求都变更的情况
import json
import urllib2
import time

DEVICEID = 7040
URL = 'http://api.miaopai.com/m/citywide_vote_for_card.json?token=WQuVt4OZaqwlsVWkmgOQ8xODGZqvsq9B&scid=jbeEXCuzFAOISK8Xbv1ZGA__&vote_type=1&deviceId=5a130c2076731109bfcb510c86242987182760'
TOTAL = 0
SUCC = 0
FAIL = 0
TIMEOUT = 0
TIMES = 15
MAX_TIME = 0
MIN_TIME =0.1
ST1 = 0
LT1 = 0
TOTAL_TIME = 0

def visit():
    
    global TOTAL
    global SUCC
    global FAIL
    global MAX_TIME
    global MIN_TIME
    global ST1
    global LT1
    global TOTAL_TIME
    global TIMEOUT


    st = time.time()
    try:
        response = urllib2.urlopen(URL+str(DEVICEID))
    except Exception:
        print "timeout"
        TIMEOUT += 1
        TOTAL += 1
    else:
        api_content = response.read()
        json_object = json.loads(api_content)
        time_span = time.time()-st

        if json_object['status'] == 200:
            TOTAL += 1
            SUCC += 1
            TOTAL_TIME += time_span
            if time_span > MAX_TIME:
                MAX_TIME = time_span
            if time_span < MIN_TIME:
                MIN_TIME = time_span
            if time_span < 1:
                ST1 += 1
            if time_span > 1:
                LT1 += 1
        else:
            TOTAL += 1
            FAIL += 1
            if time_span > MAX_TIME:
                MAX_TIME = time_span
            if time_span < MIN_TIME:
                MIN_TIME = time_span


def main():
    global DEVICEID
    print "====Test start===="

    for i in range(0, TIMES):
        DEVICEID += 1
        visit()
        time.sleep(2)

    print "Total: %s" % TOTAL
    print "Success: %s" % SUCC
    print "Fail: %s" % FAIL
    print "Timeout: %s" % TIMEOUT
    print "Max time: %s" % MAX_TIME
    print "Min time:%s" % MIN_TIME 
    if SUCC == 0:
        print "No average time because SUCC=0"
    else:
        print "Average time: %f" % (TOTAL_TIME/SUCC)
    print "Small than 1s: %s, percent: %0.2f" % (ST1, float(ST1) / TOTAL)
    print "Large than 1s: %s, percent: %0.2f" % (LT1, float(LT1) / TOTAL)

if __name__ == '__main__':
    main()
