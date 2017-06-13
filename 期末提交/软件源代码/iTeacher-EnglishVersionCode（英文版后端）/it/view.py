# -*- coding: utf-8 -*-
import random
import sys
reload(sys)
sys.setdefaultencoding('utf8')
from django.contrib import auth
from django.http import HttpResponse,HttpResponseRedirect
from model.models import Test,user,bookInfo,labels,Preference,scores
from django.shortcuts import render
from django.core.paginator import Paginator

dictionary = { 
	'0000':'Mathematics',
	'0001':'Media Tie In',
	'0002':'Usability',
	'0003':'Classics',
	'0010':'Mystery',
	'0011':'Reference',
	'0012':'Physics',
	'0013':'Parenting',
	'0014':'Climate Change',
	'0015':'Logic',
	'0020':'Philosophy',
	'0021':'Academic',
	'0022':'Theory',
	'0023':'Faith',
	'0030':'Reference',
	'0031':'Crafty',
	'0040':'Management',
	'0041':'Artificial Intelligence',
	'0042':'Audiobook',
	'0043':'Spy Thriller',
	'0044':'Technical',

	'0100':'Autobiography',
	'0101':'Mathematics',
	'0102':'Computer Science',
	'0103':'Algorithms',
	'0104':'Computers',
	'0105':'Abandoned',
	'0110':'Artificial Intelligence',
	'0111':'Language',
	'0112':'Language',
	'0113':'Technology',
	'0114':'Business',
	'0115':'Computers',
	'0116':'Internet',
	'0117':'Engineering',
	'0120':'Design',
	'0121':'Nonfiction',
	'0122':'Management',
	'0123':'Internet',
	'0124':'Usability',
	'0130':'Software',
	'0131':'Environment',
	'0132':'Language',
	'0133':'Coding',
	'0134':'Textbooks',
	'0135':'Environment',
	'0136':'Software',
	'0140':'Electrical Engineering',
	'0141':'Technical',
	'0142':'Management',
	'0143':'Electrical Engineering',
	'0144':'Usability',
	'0145':'Technical',
	'0150':'Technical',
	'0151':'Mathematics',
	'0152':'Computers',
	'0153':'Photography',
	'0154':'Photography',
	'0155':'Art Design',
	'0156':'Management',
	'0157':'Management',
	'0158':'Theory',
	'0160':'Internet'
}

randg1 = 0
randg2 = 0
class BOOK(object):
	def __init__(self,name,detail,author,imgUrl):
		self.name = name
		self.detail = detail
		self.autor = author
		self.imgUrl = imgUrl
	
def hello(request):
    context          = {}
    context['hello'] = 'Hello1 World!'
    return render(request, 'hello.html', context)

def testdb(request):
	test1 = Test(name = '111')
	test1.save()
	return HttpResponse("saved ")

def index(request):
	return indexpage(request,'0000')
	#context          = {}
	#return render(request, 'index.html', context)
def main_page(request):
	context          = {'username':request.COOKIES.get('username')}
	return render(request, 'main_page.html', context)
def test(request):
	context          = {}
	return render(request, 'test.html', context)
def test2(request):
	context          = {}
	return render(request, 'test2.html', context)
def loginpage(request):
	context          = {}
	return render(request, 'login.html', context)
def login(request):
	context          = {}
	ctx ={}
	right = 0
	if request.POST:
		ctx['username'] = request.POST['user[email]']
		ctx['userpasswd'] = request.POST['user[password]']
	usrlist = user.objects.all()
	for usr in usrlist:
		if usr.userName == ctx['username'] and usr.userPasswd == ctx['userpasswd']:
			right = 1
	if right == 1:
		response = HttpResponseRedirect('/main_page')
		response.set_cookie('username',ctx['username'],3600)
		return response		
		#return render(request,'main_page.html',ctx)
	else:
		response = HttpResponseRedirect('/')
		return response
	#return render(request, 'login.html', context)
def signup(request): 
	ctx ={}
	if request.POST:
		ctx['username'] = request.POST['user[email]']
		ctx['userpasswd'] = request.POST['user[password]']
	unitUsr = user(userName = ctx['username']+'',userPasswd = ctx['userpasswd']+'')
	unitUsr.save()
	response = HttpResponseRedirect('/main_page')
	response.set_cookie('username',ctx['username'],3600)
	return response
def sign_up_page(request):
	context          = {}
	return render(request, 'signuppage.html', context)

# 书籍列表界面
def indexpage(request,id):
	url = '119.29.246.19:7000'
	page = 0
	try:
		page = int(request.GET['page']) -1
	except:
		page = 0
	# 传入书籍标签ID，根据字典确定标签名	
	labelID = int(id)
	username = request.COOKIES.get('username','')
	thislabel = dictionary[id]
	# 获取标签对应的书籍列表
	list = labels.objects.filter(label = thislabel)	
	books = []
	context          = {}  
	# 获取所有符合标签的书籍
	for book in list:
		books.append(bookInfo.objects.get(bookID = book.bookID))
	# 完成翻页功能
	bookNum = len(books)
	pages = []
	maxPage = int (bookNum / 3) + 1
	pageEnd = min(page+3 , maxPage)
	if page > maxPage or page < 0:
		page = 0

	prePage = 0
	nextPage = 0
	if page == 0:
		prePage = 1
	else:
		prePage = page
	if page == maxPage - 1:
		nextPage = maxPage
	else:
		nextPage = page + 2
	
	start = page * 3
	end = min(bookNum,start + 3)
	indexBooks = books[start : end]

	for i in range(pageEnd - page):
		pages.append(str(page+1+i))
	context = {'username':username,'label':thislabel,'books' : indexBooks,'pages':pages,'prePage':prePage,'nextPage':nextPage,'url':url} 
	return render(request, 'index.html', context)  

# 书本详细内容页面
def content(request,id):
	if request.method == 'GET':
		try:
			bookID = request.GET['bookID']
			username = request.COOKIES.get('username','')	
			context          = {}  
			book = bookInfo.objects.get(bookID = bookID)
			commentList = Preference.objects.filter(bookID = bookID)
			context = {'book':book,'username':username,'commentList':commentList }
			return render(request, 'content.html', context) 
		except:
			bookID = 0
# 登出功能
def logout(req):
	response = HttpResponseRedirect('/')
	response.delete_cookie('username')
	return response
def logout2(req,id):
	response = HttpResponseRedirect('/')
	response.delete_cookie('username')
	return response
# 用户发表评论功能
def comment(request,id,book_id):
	books = bookInfo.objects.all()
	path = '/index/'+id +'/content/?bookID=' + book_id
	response = HttpResponseRedirect(path)
	ctx = {}
	ctx['username'] = request.COOKIES.get('username','')
	if request.POST:	
		ctx['comments'] = request.POST['comments'] 
	if ctx['comments'] == '': 
		return response
	bookID = int(book_id)
	comment = Preference(userName = ctx['username'],bookID = bookID,comments = ctx['comments'])
	comment.save()
	return response 
# 用户评分功能
def saveScore(request,id,bookid,score):
	path = '/index/'+id+'/content/?bookID='+bookid
	response = HttpResponseRedirect(path)
	username = request.COOKIES.get('username','')
	bookID = int(bookid)
	try:
		one_score = scores(userName = username,score = score,bookID = bookID)
		one_score.save()
	except:
		context          = {} 
	return response