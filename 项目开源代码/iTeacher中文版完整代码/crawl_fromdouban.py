#_*_ coding: utf-8_*_

import urllib2
import os
import pickle
import numpy
import re
import sqlite3
bookID = 0
Top_Url="https://book.douban.com"
Url_Pre="https://book.douban.com/subject_search?start="

Url_Mid="&search_text="

Url_Post="&cat=1001"
Url_Post2=""

Crawl_Url=""

current_number=0


All_Book=[]

count=1


def open_url(url):
    req = urllib2.Request(url)
    req.add_header('User-Agent',
                   'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.75 Safari/537.36 QQBrowser/4.1.4132.400')
    response = urllib2.urlopen(req)
    print(url)
    return response.read().decode('utf-8')

def get_one_book_infomation(url):

    global All_Book
    html=open_url(url)

    start=html.find('v:itemreviewed')+16
    end=html.find('</span>',start)
    title=html[start:end]
    print 'title'+title


    pre=html.find('<div id="info" class="">')
    pre=html.find('<span class="pl">',pre)
    start=html.find('>',pre+30)+1
    end=html.find('<',start)
    author=html[start:end]
    author="".join(author.split())

    print 'author'+author


    pre=html.find('<div class="intro">')
    pre2=html.find('<div class="intro">',pre+10)
    if pre2!=-1:
        pre=pre2
    end=html.find('</div>',pre)
    content=html[pre:end]

    dr = re.compile(r'<[^>]+>', re.S)
    content = dr.sub('', content).strip()

    if content=='':
        return

    print 'content'+content


    intro=''
    pre = html.find('<div id="info" class="">')
    last = html.find('</div>', start)

    start=html.find('<span class="pl">',pre,last)
    start = html.find('<span class="pl">', start+1, last)

    while start!=-1:
        end=html.find('<br',start)
        end=html.find('>',end)+1
        temp=html[start:end]
        temp = dr.sub('', temp)
        temp="".join(temp.split())
        intro=intro+temp+'/'

        start=html.find('<span class="pl">',end,last)
    if intro=='':
        return

    print 'introduction:' + intro



    pre=html.find('class="nbg"')
    start=html.find('href="',pre)+6
    end=html.find('"',start)
    img_url=html[start:end]
    print 'img_url'+img_url


    label=[]
    pre=html.find('db-tags-section')
    pre=html.find('<a class="  tag"',pre)
    while pre!=-1:
        start=html.find('>',pre)+1
        end=html.find('</a>',start)
        label.append(html[start:end])

        pre=html.find('<a class="  tag"',end)

    if len(label)==0:
        return
    print 'label:'+label[0]


    global bookID
    bookID += 1
    temp_info={'book_title':title,'author':author,'introduction':intro,'content':content,'img_url':img_url,'label':label,'bookID':bookID}
    All_Book.append(temp_info)


def crawl_in_onepage(url):
    global current_number
    global count
    html = open_url(url)

    pre=html.find('nbg')


    while pre!=-1:

        start = html.find('href="', pre) + 6
        end = html.find('"', start)
        get_one_book_infomation(html[start:end])
        pre=html.find('nbg',end)


    pre = html.find('class="next"')
    if html.find('next', pre + 10, pre + 50) == -1:
        print '结束爬虫'
        return
    else:
        if count<=current_number/15+1:
            print '结束爬虫'
            return
        else:
            current_number += 15
            print current_number

            crawl_in_onepage(Url_Pre+str(current_number)+Url_Post2)




def crawl_from_douban(search, page_number):
    global current_number
    global Url_Post2
    global count
    count=page_number
    Url_Post2=Url_Mid+search+Url_Post
    Crawl_Url=Url_Pre+str(current_number)+Url_Post2
    crawl_in_onepage(Crawl_Url)

    return All_Book

if __name__=="__main__":
    conn = sqlite3.connect('db.sqlite3')
    dictionary = ['人工智能理论']
    dictionary2 = [u'人工智能理论',
                  u'自动机理论',
                  u'可计算性理论',
                  u'计算机可靠性理论',
                  u'算法理论',
                  u'数据结构',
                  u'数据安全与计算机安全',
                  u'人工智能理论',
                  u'自然语言理解与机器翻译',
                  u'自然语言处理',
                  u'机器翻译',
                  u'模式识别',
                  u'计算机感知',
                  u'计算机神经网络',
                  u'知识工程',
                  u'计算机系统设计',
                  u'并行处理',
                  u'分布式处理系统',
                  u'计算机网络',
                  u'计算机运行测试与性能评价',
                  u'软件理论',
                  u'操作系统与操作环境',
                  u'程序设计及其语言',
                  u'编译系统',
                  u'数据库',
                  u'软件开发环境与开发技术',
                  u'软件工程',
                  u'计算机元器件',
                  u'计算机处理器技术',
                  u'计算机存储技术',
                  u'计算机外围设备',
                  u'计算机制造与检测',
                  u'计算机高密度组装技术',
                  u'计算机应用技术',
                  u'文字信息处理',
                  u'计算机仿真',
                  u'计算机图形学',
                  u'计算机图象处理',
                  u'计算机辅助设计',
                  u'计算机过程控制',
                  u'计算机信息管理系统',
                  u'计算机决策支持系统'
                  ]
    for i in range(len(dictionary)):
        books = crawl_from_douban(dictionary[i],1)
        for book in books:
            conn.execute("INSERT INTO model_bookinfo (bookID,bookName,bookDetail,imgUrl,author,bookIntro ) VALUES (?,?,?,?,?,?)",(book['bookID'],book['book_title'],book['content'],book['img_url'],book['author'],book['introduction']))
            # for label in book['label']:
            #     conn.execute("INSERT INTO model_labels (bookID,label) VALUES (?,?)",(book['bookID'],label))
            conn.execute("INSERT INTO model_labels (bookID,label) VALUES (?,?)",(book['bookID'],dictionary[i]))
    conn.commit()
    conn.close()