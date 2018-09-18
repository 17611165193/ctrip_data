# coding: UTF-8
import re
import sys
from urllib import urlopen

reload(sys)
sys.setdefaultencoding( "utf-8" )

def InsertDict(D, key, value):
    D.setdefault(key)
    D[key] = value


def GetHtml(url):
    response = urlopen(url)
    text = response.read().decode('gbk')
    return text


def GetDict(s, D1):
    for i in range(len(s)):
        s0 = s[i].split('(')
        s1 = s0[0]
        s2 = s0[1].replace(')', '')
        InsertDict(D1, s1, s2)


def GetCitycode(original_city, D):
    for k in D:
        if original_city == k:
            return D[k]
        else:
            pass


def UrlJoin(original_city_code, target_city_code, t):
    return 'http://flights.ctrip.com/domestic/ajax/Get90DaysLowestPrice?dcity=%s&acity=%s&ddate=%s&searchType=S&r=0.18035678380179632' % (original_city_code, target_city_code, t)


def GetLowestprice(lowerprice_html, D2, time):
    L = re.findall(r'[0-9]{4}\-[0-9]{2}\-[0-9]{2}', lowerprice_html)
    L1 = re.findall(r'\d{3,4}', lowerprice_html)
    L2 = []
    for i in range(len(L1)):
        if int(L1[i]) == 2017 or int(L1[i]) == 2018:
            pass
        else:
            L2.append(L1[i])
    for i in range(len(L)):
        InsertDict(D2, L[i], L2[i])
    print('%s最低票价: %sRMB'%(time, D2[time]))

D1 = {}
D2 = {}
get_citycode_url = 'http://webresource.c-ctrip.com/code/cquery/resource/address/flight/flight_new_poi_gb2312.js?CR_2018_06_21_18_00_00'
citycode_html = GetHtml(get_citycode_url)
s = re.findall(u"[\u4e00-\u9fa5]+\([A-Z]+\)", citycode_html)
GetDict(s, D1)
original_city = input('请输入出发地：')
target_city = input('请输入目的地：')
time = input('请输入时间：')
original_city_code = GetCitycode(original_city, D1)
target_city_code = GetCitycode(target_city, D1)
get_lowerprice_url = UrlJoin(original_city_code, target_city_code, time)
lowerprice_html = GetHtml(get_lowerprice_url)
get_lowest = GetLowestprice(lowerprice_html, D2, time)
target_url = 'http://flights.ctrip.com/booking/%s-%s-day-1.html?DDate1=%s' % (original_city_code, target_city_code, time)
print(target_url)