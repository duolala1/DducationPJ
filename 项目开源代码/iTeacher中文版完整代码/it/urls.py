"""it URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls.static import static, settings
from django.conf.urls import url
from django.contrib import admin
from . import view
urlpatterns = [
    url(r'^test$',view.getCollection),
    url(r'^textClassification/$',view.classifyText),
    url(r'^admin/', admin.site.urls),
    url(r'^testdb$',view.testdb),
    url(r'^index/$',view.index),
    url(r'^main_page$',view.main_page),
    url(r'^test$',view.test),
    url(r'^test2$',view.test2),
    url(r'^$',view.loginpage),
    url(r'^signup/$',view.signup),
    url(r'^sign_up_page/$',view.sign_up_page), 
    url(r'^login/$',view.login),
    url(r'^index/(?P<id>\d{4})/$',view.indexpage),
    url(r'^index/(?P<id>\d{4})/collect/$',view.saveCollection),
    url(r'^index/(?P<id>\d{4})/search/$',view.searchRedirect),
    url(r'^index/search/$',view.search),
    url(r'^index/search/search/$',view.urlRed),
    url(r'^index/search/content/$',view.content),
    url(r'^index/search/content/comment/(\d+)/$',view.slComment),
    url(r'^index/search/content/(\d+)/score/(\d+)/$',view.slSaveScore),
    url(r'^index/(?P<id>\d{4})/content/$',view.content),
    url(r'^index/(\d+)/content/(\d+)/score/(\d+)/$',view.saveScore),
    url(r'^index/sign_out$',view.logout),
    url(r'^index/(?P<id>\d{4})/sign_out$',view.logout2),
    url(r'^index/personal/$',view.personal),
    url(r'^index/personal/delc/$',view.delCollection),
    url(r'^index/personal/delh/$',view.delHistory),
    url(r'^index/(\d+)/content/comment/(\d+)/$',view.comment),


]
