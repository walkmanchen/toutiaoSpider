# coding=utf-8

import requests
from bs4 import BeautifulSoup
import re
from fake_useragent import UserAgent
from pymysql import *
import time

'''
今日头条号主description信息抓取
'''

def get_content(openid):
    ua = UserAgent()
    url = 'http://m.toutiao.com/profile/' + str(openid) + '/'
    headers = {
        'User-Agent': ua.random,
    }

    body = requests.get(url,headers=headers).text
    time.sleep(0.1)
    response = BeautifulSoup(body,'lxml')

    try:
        soup = response.find_all('p',{'id':'description'})[0]
        soup2 = BeautifulSoup(str(soup), 'lxml')
        desc = soup2.get_text()
        print(desc)
    except:
        desc = '[]'
    time.sleep(0.1)

    return desc

if __name__ == '__main__':
    db = connect(host='localhost', port=3306, db='spider', user='root', password='secret',charset='utf8')
    cursor = db.cursor()
    try:
        sql = """select id,openid,flag,`describe` from jjb_media"""
        cursor.execute(sql)
        data = cursor.fetchall()
        db.commit()
    except:
        db.rollback()

    for i in range(len(data)):
        id = data[i][0]
        flag = data[i][2]
        desc = data[i][3]
        if flag == '今日头条' and desc == '[]':
            print(id)
            #uid = data[i][1]
            #con = get_content(uid)
            con = ''
            param = [con, id]
            try:
                sql = """update jjb_media set `describe` = %s where id = %s"""
                cursor.execute(sql, param)
                db.commit()
                print('ok!!!!!')
            except:
                db.rollback()
        else:
            pass

    db.close()