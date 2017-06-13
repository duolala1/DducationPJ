#_*_ coding: utf-8_*_

import urllib2
import sqlite3
import os
import pickle
import numpy
import re

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
    return response.read().decode('utf-8')

def get_one_book_infomation(url):

    global All_Book
    html=open_url(url)

    start=html.find('v:itemreviewed')+16
    end=html.find('</span>',start)
    title=html[start:end]


    pre=html.find('<div id="info" class="">')
    pre=html.find('<span class="pl">',pre)
    start=html.find('>',pre+30)+1
    end=html.find('<',start)
    author=html[start:end]
    author="".join(author.split())



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




    pre=html.find('class="nbg"')
    start=html.find('href="',pre)+6
    end=html.find('"',start)
    img_url=html[start:end]


    label=[]
    pre=html.find('db-tags-section')
    pre=html.find('<a class="  tag"',pre)
    while pre!=-1:
        start=html.find('>',pre)+1
        end=html.find('</a>',start)
        label.append(html[start:end])


    if len(label)==0:
        return



    global bookID
    bookID =bookID + 1

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
        return
    else:
        if count<=current_number/15+1:
            return
        else:
            current_number += 15
            print (current_number)

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
    books = crawl_from_douban('人工智能理论',1)
    books = []
    books.append({'book_title':'diyi','author':'diyi','introduction':'diyi','content':'diyi','img_url':'diyi','label':'diyi','bookID':0})
    for book in books:
        conn.execute("INSERT INTO model_bookinfo (bookID,bookName,bookDetail,imgUrl,author,bookIntro ) VALUES (?,?,?,?,?,?)",(book['bookID'],book['book_title'],book['content'],book['img_url'],book['author'],book['introduction']));
    conn.commit()
    conn.close()