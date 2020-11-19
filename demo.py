#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/11/3 20:37
# @Author  : 黄林杰
# @File    : demo.py
# @Software: PyCharm

from bs4 import BeautifulSoup
import re
import urllib.request,urllib.error
import xlwt
import sqlite3

#影片详情的规则
findlink = re.compile(r'<a href="(.*?)">')              #创建正则表达式，表示规则（字符串的模式）
#影片的图片
findImgSrc = re.compile(r'<img.*src=(.*?)"',re.S)
#影片片名
findTitle = re.compile(r'<span class="title">(.*)</span>')
#影片评分
findRating = re.compile(r'<span class="rating_num" property="v:average">(.*)</span>')
#影片评价人数
findJudge =re.compile(r'<span>(\d*)人评价</span>')
#影片概况
findInq = re.compile(r'<span class="inq">(.*)</span>')
#影片的相关内容
findBd = re.compile(r'<p class="">(.*?)</p>',re.S)


#主程序
def main():
    baseurl = "https://movie.douban.com/top250?start="
    savapath = "豆瓣电影Top250.xls"
    #1.爬取网页
    datalist = getData(baseurl)

    saveData(datalist,savapath)


    #3.保存数据

#爬取网页
def getData(baseurl):
    datalist = []
    for i in range(0,10):           #调用获取页面信息的函数，10次
        url=baseurl+str(i*25)
        html = askurl(url)



    # 2.逐一解析数据


        soup = BeautifulSoup(html,"html.parser")
        for item in soup.find_all('div',class_="item"):
            data = []    #保存一部电影的所有信息
            item = str(item)

            #影片详情的链接
            link = re.findall(findlink,item)[0]              #re库用来通过正则表达式查找指定的字符串
            data.append(link)
            imgSrc = re.findall(findImgSrc,item)[0]
            data.append(imgSrc)
            title = re.findall(findTitle,item)
            if(len(title)==2):
                ctitle = title[0]
                data.append(ctitle)
                otitle = title[1].replace("/","")
                data.append(otitle)
            else:
                data.append(title[0])
                data.append(' ')

            rating = re.findall(findRating,item)[0]
            data.append(rating)

            judgeNum =re.findall(findJudge,item)[0]
            data.append(judgeNum)

            inq = re.findall(findInq,item)
            if len(inq)!=0:
                inq = inq[0].replace("。","")
                data.append(inq)
            else:
                data.append(" ")

            bd = re.findall(findBd,item)[0]
            bd = re.sub('<br(\s?)/>(\s+)?'," ",bd)
            bd = re.sub('/',' ',bd)
            data.append(bd.strip())
            datalist.append(data)
    return datalist



def askurl(url):
    head = {

        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36"
    }

    request = urllib.request.Request(url,headers=head)
    html = ''
    try:
        response = urllib.request.urlopen(request)
        html = response.read().decode("utf-8")
        # print(html)
    except urllib.error.URLError as e:
        if hasattr(e,"code"):
            print(e.code)
        if hasattr(e,"reason"):
            print(e.reason)
    return html


#保存数据
def saveData(datalist,savepath):
    print("save...")
    book = xlwt.Workbook(encoding="utf-8",style_compression=0)
    sheet = book.add_sheet('豆瓣电影Top250',cell_overwrite_ok=True)
    col = ("电影详情链接","图片链接","影片中文名","影片外国名","评分","评分数","概况","相关信息")
    for i in range(0,8):
        sheet.write(0,i,col[i])
    for i in range(0,250):
        print("第%d条"%(i+1))
        data = datalist[i]
        for j in range(0,8):
            sheet.write(i+1,j,data[j])

    book.save(savepath)





if __name__ == '__main__':
    main()

