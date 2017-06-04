# -*- coding: utf-8 -*-
import random
import sys
reload(sys)
sys.setdefaultencoding('utf8')
from django.contrib import auth
from . import textClassify
from django.http import HttpResponse,HttpResponseRedirect
from model.models import Test,user,bookInfo,labels,Preference,scores,Interests,Collection,History,Recommend
from django.shortcuts import render
from django.core.paginator import Paginator
import pickle
from . import sort
dictionary = {
u'0000':'信息论概念',
'0001':'信息理论与信息系统',
'0002':'控制论',
'0003':'系统论',
'0010':'混沌',
'0011':'一般系统论',
'0012':'耗散结构理论',
'0013':'协同学',
'0014':'突变论',
'0015':'超循环论',
'0020':'大系统理论',
'0021':'系统辩识',
'0022':'状态估计',
'0023':'鲁棒控制',
'0030':'系统工程基本条目',
'0031':'系统建模',
'0040':'控制论',
'0041':'模式识别与智能系统',
'0042':'导航',
'0043':'制导与控制',
'0044':'过程装备与控制工程',
'0100':'自动机理论',
'0101':'可计算性理论',
'0102':'计算机可靠性理论',
'0103':'算法理论',
'0104':'数据结构',
'0105':'数据安全与计算机安全',
'0110':'人工智能理论',
'0111':'自然语言理解与机器翻译',
'0112':'自然语言处理',
'0113':'机器翻译',
'0114':'模式识别',
'0115':'计算机感知',
'0116':'计算机神经网络',
'0117':u'知识工程',
'0120':'计算机系统设计',
'0121':'并行处理',
'0122':'分布式处理系统',
'0123':'计算机网络',
'0124':'计算机运行测试与性能评价',
'0130':'软件理论',
'0131':'操作系统与操作环境',
'0132':'程序设计及其语言',
'0133':'编译系统',
'0134':'数据库',
'0135':'软件开发环境与开发技术',
'0136':'软件工程',
'0140':'计算机元器件',
'0141':'计算机处理器技术',
'0142':'计算机存储技术',
'0143':'计算机外围设备',
'0144':'计算机制造与检测',
'0145':'计算机高密度组装技术',
'0150':'计算机应用技术',
'0151':'文字信息处理',
'0152':'计算机仿真',
'0153':'计算机图形学',
'0154':'计算机图象处理',
'0155':'计算机辅助设计',
'0156':'计算机过程控制',
'0157':'计算机信息管理系统',
'0158':'计算机决策支持系统',
'0160':'网络工程',
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
	test1 = Test(name = '试试啊')
	test1.save()
	test2 =Test.objects.all()
	return HttpResponse(test2[0].name)

def index(request):
	return indexpage(request,'0000')
	#context          = {}
	#return render(request, 'index.html', context)
def main_page(request):
	if request.COOKIES.get('username','') == '':
		return HttpResponseRedirect('119.29.246.19:8888')
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

# 处理用户注册请求
def signup(request): 
	global dictionary
	ctx ={}
	pref = []
	if request.POST:
		ctx['username'] = request.POST['user[email]']
		ctx['userpasswd'] = request.POST['user[password]']
		# 记录用户偏好
		for ele in request.POST:
			for index in dictionary:
				if dictionary[index] == ele:
					pref.append(ele)
	# 保存用户偏好
	for entry in pref:
		preference = Interests(userName = ctx['username'], label = entry)
		preference.save()
	generateRecommends(ctx['username'])
	unitUsr = user(userName = ctx['username']+'',userPasswd = ctx['userpasswd']+'')
	unitUsr.save()
	response = HttpResponseRedirect('/main_page')
	response.set_cookie('username',ctx['username'],3600)
	return response

# 保存产生用户偏好目录
def generateRecommends(username):
	list = Interests.objects.filter(userName = username)
	for entry in list:
		label = entry.label
		temp_list = labels.objects.filter(label = label)
		for ele in temp_list:
			recBook = Recommend(bookID = ele.bookID,userName = username)
			recBook.save()
			
	
# 显示用户注册界面
def sign_up_page(request):
	context          = {}
	global dictionary
	dic = []
	for ele in dictionary:
		dic.append(dictionary[ele])
	context['dic'] = dic[:12] 
	return render(request, 'signuppage.html', context)

# 书籍列表界面
def indexpage(request,id):
	if request.COOKIES.get('username','') == '':
		return HttpResponseRedirect('119.29.246.19:8888')
	url = '119.29.246.19:8888'
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
# 用户浏览历史记录功能 
def saveHistory(username,bookID):
	alreadyIn = False
	entries = History.objects.all()
	for ele in entries:	# 判断是否重复
		if ele.userName == username and ele.bookID == bookID:
			alreadyIn = True

	if not alreadyIn:
		entry = History(userName=username,bookID = bookID)
		entry.save()

def getHistory(request):
	username = request.COOKIES.get('username','')
	list = History.objects.filter(userName=username)
	book_list = []
	for entry in list:
		book_list.append(entry.bookID)
	return HttpResponse(book_list)

def delHistory(request):
	if request.GET:
		bookID = request.GET['bookID']
	username = request.COOKIES.get('username','')
	History.objects.get(userName = username,bookID = bookID).delete()
	return HttpResponseRedirect('/index/personal/')
	
# 用户收藏功能
def saveCollection(request,id):
	if request.GET:
		bookID = request.GET['bookID']
		username = request.COOKIES.get('username','')
	collection = Collection(userName = username,bookID = bookID)
	alreadyIn = False
	collections = Collection.objects.all()
	for ele in collections:
		if ele.userName == username and ele.bookID == bookID:
			alreadyIn = True
	if not alreadyIn:
		collection.save()
	return HttpResponseRedirect('/index/'+id )

def getCollection(request):
	username = request.COOKIES.get('username','')
	list = Collection.objects.filter(userName=username)
	book_list = []
	for entry in list:
		book_list.append(entry.bookID)
	return HttpResponse(book_list)

def delCollection(request):
	if request.GET:
		bookID = request.GET['bookID']
	username = request.COOKIES.get('username','')
	Collection.objects.get(userName = username,bookID = bookID).delete()
	return HttpResponseRedirect('/index/personal/')
	
# 书本详细内容页面（根据标签）
def content(request,id='0'):
	if request.COOKIES.get('username','') == '':
		return HttpResponseRedirect('119.29.246.19:8888')
	url = '119.29.246.19:8888'
	if request.method == 'GET':
		try:
			bookID = request.GET['bookID']
			username = request.COOKIES.get('username','')	
			saveHistory(username,bookID)	# 用户访问后保存记录
			context          = {}  
			book = bookInfo.objects.get(bookID = bookID)
			commentList = Preference.objects.filter(bookID = bookID)
			context = {'book':book,'username':username,'commentList':commentList,'url':url }
			return render(request, 'content.html', context) 
		except:
			name = request.GET['q']
			page = 0
			redirectUrl =  '/index/search/?' + 'item=' + name +'&' + 'page=' + str(page)
			return HttpResponseRedirect(redirectUrl)	

# 个人信息页面
def personal(request):
	if request.COOKIES.get('username','') == '':
		return HttpResponseRedirect('119.29.246.19:8888')
	url = '119.29.246.19:8888'
	username = request.COOKIES.get('username','')	
	context          = {}  
	# 加载用户个人历史纪录
	temp_his_list = History.objects.filter(userName = username)
	his_list = []
	for entry in temp_his_list:
		if entry.bookID != '':
			try:
				his_list.append(bookInfo.objects.get(bookID = entry.bookID))
			except:
				print entry
	his_list_r = his_list[:]
	length = len(his_list)
	for i in range(length):
		his_list_r[i] = his_list[length - 1 - i]
	if length >= 10:
		his_list = his_list[:9]
	
	# 加载用户个人收藏
	temp_clt_list = Collection.objects.filter(userName = username)
	clt_list = []
	for entry in temp_clt_list:
		if entry.bookID != '':
			clt_list.append(bookInfo.objects.get(bookID = entry.bookID))

	# 加载用户个人推荐
	temp_rec_list = Recommend.objects.filter(userName = username)
	rec_list = []
	for entry in temp_rec_list:
		if entry.bookID != '':
			rec_list.append(bookInfo.objects.get(bookID = entry.bookID))
	if len(rec_list) >= 15:
		rec_list = rec_list[:14]
	# 加载个人偏好
	temp_int_list = Interests.objects.filter(userName = username)
	int_list = []
	for entry in temp_int_list:
		int_list.append(entry.label)
	context = {'username':username,'url':url,'history':his_list_r,'collects':clt_list,'recommends':rec_list,'interests':int_list}
	return render(request, 'personal.html', context) 		

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

# 用户发表评论功能(搜索出的列表）
def slComment(request,book_id):
	books = bookInfo.objects.all()
	path = '/index/search/content/?bookID=' + book_id
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
# 用户评分功能(搜索结果列表）
def slSaveScore(request,bookid,score):
	path = '/index/search/content/?bookID='+bookid
	response = HttpResponseRedirect(path)
	username = request.COOKIES.get('username','')
	bookID = int(bookid)
	try:
		one_score = scores(userName = username,score = score,bookID = bookID)
		one_score.save()
	except:
		context          = {} 
	return response
def classifyText(request):
	label_file = file('labels','rb')
	label_list = pickle.load(label_file)
	testText = [" John E.Hopcroft 于斯坦福大学获得博士学位，现为康奈尔大学计算机科学系教授。1994年到2001年，任康奈尔大学工程学院院长。他是1986年图灵奖获得者。他的研究兴趣集中在计算理论方面，尤其是算法分析、自动机理论等。 Rajeev Motwani 于加州大学伯克利分校获得博士学位，现为斯坦福大学计算机科学系教授。他的研究兴趣包括：数据库、数据挖掘，Web搜索和信息检索、机器人等。 Jeffrey D. Ullman 斯坦福大学计算机科学系 Stanford W. Ascherman 教授，数据库专家，美国国家工程院院士。他的研究兴趣包括：数据库理论、数据库集成、数据挖掘、理论计算等。来的科技产品，将会是人类智慧的“容器”。"]
	
	if request.POST:
		testText = [request.POST['text']]

	result = textClassify.makePrediction(testText)
	label_index = sort.getTopIndex(result[0],3)
	result_labels = []
	for index in label_index:
		result_labels.append(label_list[index])
	return HttpResponse(result_labels)
# 搜索功能跳转
def searchRedirect(request,id):
	name = ''
	if request.GET:
		name = request.GET['item']
	page = 0
	try:
		page = int(request.GET['page']) -1
	except:
		page = 0	
	redirectUrl =  '/index/search/?' + 'item=' + name +'&' + 'page=' + str(page)
	return HttpResponseRedirect(redirectUrl)
# 搜索功能跳转
def urlRed(request):
	name = ''
	if request.GET:
		name = request.GET['item']
	page = 0
	try:
		page = int(request.GET['page']) -1
	except:
		page = 0	
	redirectUrl =  '/index/search/?' + 'item=' + name +'&' + 'page=' + str(page)
	return HttpResponseRedirect(redirectUrl)
# 搜索页面
def search(request):
	if request.COOKIES.get('username','') == '':
		return HttpResponseRedirect('119.29.246.19:8888')
	name = ''
	if request.GET:
		name = request.GET['item']
		page = int(request.GET['page'])
	bookList = bookInfo.objects.filter(bookName__contains=name)
	books = []
	for book in bookList:
		books.append(book)
	url = '119.29.246.19:8888'
	username = request.COOKIES.get('username','')
	context          = {}  
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
	context = {'username':username,'label':name,'books' : indexBooks,'pages':pages,'prePage':prePage,'nextPage':nextPage,'url':url} 
	return render(request, 'index.html', context)  
