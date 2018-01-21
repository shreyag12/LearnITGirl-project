# -*- coding: utf-8 -*-
from __future__ import unicode_literals
#from login.forms import *
from bookmark.forms import signUpForm
from django.http import HttpResponseRedirect,HttpResponse
from django.shortcuts import render,redirect
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth import authenticate,login
from .forms import UserLoginForm
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Category,UserBookmark
from itertools import chain
from taggit.models import Tag
import ast
# Create your views here.

def index(request):
        return render(
        request,
        'index.html',
    )
def register(request):
    if request.method == 'POST':
        form = signUpForm(request.POST) # Create a form instance and populate it with data from the request (binding):
        if form.is_valid():
            user = form.save()
            request.session['user'] = user.pk
            return render(request,'category.html')
# If this is a GET (or any other method) create the default form.
    else:
        form = signUpForm()
    return render(request, 'register.html', {'form': form})
def login_view(request):
    form = UserLoginForm(request.POST)
    if form.is_valid():
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        user = authenticate(username = username,password = password)
        # args = user
        args = {'user': request.user}
        login(request,user)
        blist = get_bookmark(user)
        firstname = get_firstname(request)
        return render(request,'myprofile.html',{'blist': blist,'firstname':firstname})
    return render(request,'login.html',{'form': form})

def register_success(request):
    return render(
        request,
        'success.html',
        )
    
def home_redirect(request):
    return redirect('/bookmark/')

def get_category(request):
    clist = request.POST.getlist("categories")
    user = request.session.get('user')
    print clist
    print user
    obj=Category(user_id=user,category=clist)
    obj.save()
    messages.add_message(request, messages.SUCCESS, 'Registeration succesful!')
    return render(request,'index.html')
    # user.category=cname
    # user.save()
def save_bookmark(request):
    bmark = request.POST.get("url")
    user = request.user.pk
    obj = UserBookmark(user_id=user,bookmark=bmark)
    obj.save()
    blist = get_bookmark(user)
    firstname = get_firstname(request)
    return render(request,'myprofile.html',{'blist': blist,'firstname':firstname})

def get_bookmark(user):
    blist = UserBookmark.objects.filter(user = user)
    return blist

def home(request):
    category=Category.objects.values_list('category',flat = True).filter(user=request.user.pk)
    category = list(category)
    category2=ast.literal_eval(category[0])
    print category2
    # category = category.split(',')
    # category2 = []
    # for x in category:
    #     category2.append(x)
    # # category2 = category[1:]
    # category2.encode("utf8")
    # print category2
    # print type(category)

    # bookmarks= UserBookmark.objects.values('bookmark').filter(tag__in = category).exclude(user=request.user.pk)
    # bookmarks = UserBookmark.objects.values('bookmark').filter(tag__in = ['java','android','python'])
    bookmarks = UserBookmark.objects.filter(tag__name__in = category2).exclude(user = request.user.pk).distinct()
    interests = Category.objects.values_list('category').filter(user = request.user.pk)
    interests = list(interests)
    interests= ast.literal_eval(interests[0][0])
    blist = UserBookmark.objects.values('bookmark').filter(tag__name__in = category2).exclude(user = request.user.pk).distinct()
    print blist
    mydict = {}
    for i in blist:
        tag_ids = UserBookmark.objects.values('tag').filter(bookmark = i['bookmark'])
        bookmark = i['bookmark']
        tags = Tag.objects.values_list('name',flat=True).filter(id__in = tag_ids)
        tags = list(tags)
        new = []
        for t in tags:
            n=t.encode('ascii')
            new.append(n)
        mydict[bookmark]=new
        # pair = { bookmark, tags}
        # mydict.append(pair)
    # tag_ids = UserBookmark.objects.values('tag').filter(bookmark__in = blist)
    # tags = Tag.objects.filter(id__in = tag_ids)
    # print mydict
    # for key in mydict:
    #     print mydict[key]
    # firstname = User.objects.values_list('first_name').filter(username= request.user.username)
    # firstname = list(firstname)
    # firstname = str(firstname[0][0])
    firstname = get_firstname(request)
    return render(request,'home.html',{'mydict': mydict,'bookmarks' :bookmarks, 'interests':interests,'firstname':firstname})
    # return render(request,'home.html',{'mydict':mydict})

def save_tag(request):
    tagslist = request.POST.get("tag")
    tagslist = tagslist.split(',')
    bookmark = request.POST.get("bookmark")
    print tagslist
    obj=UserBookmark.objects.get(bookmark = bookmark)
    user = request.user.pk
    # obj.tag = tagslist
    obj.tag.add(*tagslist)
    obj.save()
    blist = get_bookmark(user)
    return render(request,'myprofile.html',{'blist' : blist})

def delete_bookmark(request,bookmark):
    user = request.user.pk
    # bookmark = request.POST.get("value")
    UserBookmark.objects.filter(user = user,bookmark = bookmark).delete()
    blist = get_bookmark(user)
    firstname = get_firstname(request)
    return render(request,'myprofile.html',{'blist' : blist,'firstname':firstname})
def add_bookmark(request,bookmark): 
    user = request.user.pk
    obj=UserBookmark(user_id=user,bookmark = bookmark)
    obj.save()
    bookmarks = show(user)
    mydict = get_dict(request)
    interests = get_interest(request)
    firstname = get_firstname(request)
    return render(request,'home.html',{'mydict': mydict,'bookmarks' :bookmarks, 'interests':interests,'firstname':firstname})

def show(user):
    category=Category.objects.values_list('category',flat = True).filter(user=user)
    category = list(category)
    category2=ast.literal_eval(category[0])
    bookmarks = UserBookmark.objects.filter(tag__name__in = category2).exclude(user = user).distinct()
    return bookmarks
def profile(request):
    user = request.user.pk
    blist = get_bookmark(user)
    firstname = get_firstname(request)
    print firstname
    return render(request,'myprofile.html',{'blist': blist,'firstname':firstname})
def about(request):
    return render(request,'about.html')
def get_firstname(request):
    firstname = User.objects.values_list('first_name').filter(username= request.user.username)
    firstname = list(firstname)
    firstname = str(firstname[0][0])
    return firstname
def get_dict(request):
    category=Category.objects.values_list('category',flat = True).filter(user=request.user.pk)
    category = list(category)
    category2=ast.literal_eval(category[0])
    interests = Category.objects.values_list('category').filter(user = request.user.pk)
    interests = list(interests)
    interests= ast.literal_eval(interests[0][0])
    blist = UserBookmark.objects.values('bookmark').filter(tag__name__in = category2).exclude(user = request.user.pk)
    mydict = {}
    for i in blist:
        tag_ids = UserBookmark.objects.values('tag').filter(bookmark = i['bookmark'])
        bookmark = i['bookmark']
        tags = Tag.objects.values_list('name',flat=True).filter(id__in = tag_ids)
        tags = list(tags)
        new = []
        for t in tags:
            n=t.encode('ascii')
            new.append(n)
        mydict[bookmark]=new
    return mydict
def get_interest(request):
    interests = Category.objects.values_list('category').filter(user = request.user.pk)
    interests = list(interests)
    interests= ast.literal_eval(interests[0][0])
    return interests





