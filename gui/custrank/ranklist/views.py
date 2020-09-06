from django.shortcuts import render,redirect
import requests
from lxml import html
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from .forms import *
from .models import Person
from django.db.models import Q

def home(request):
    usersobj = Person.objects.all()
    users=[]
    for i in usersobj:
        users.append(i.name)
    ranklist={}
    for i in users:
        URL = 'https://leetcode.com/'+i+'/'
        page = requests.get(URL)
        tree = html.fromstring(page.content)
        solved = tree.xpath('//span[@class="badge progress-bar-success"]/text()')
        if(len(solved)==7):
            ranklist[i]=int(solved[1].strip().split(" ")[0])
        else:
            ranklist[i]=int(solved[3].strip().split(" ")[0])
    ranklist={k: v for k, v in sorted(ranklist.items(), key=lambda item: item[1],reverse=True)}
    if 'analyse' in request.POST: #get time and redirect to next page
        name = add(request.POST)
        if name.is_valid():
            username=name.cleaned_data['Username']
            URL = 'https://leetcode.com/'+username.strip()+'/'
            page = requests.get(URL)
            tree = html.fromstring(page.content)
            solved = tree.xpath('//span[@class="badge progress-bar-success"]/text()')
            print(len(solved))
            if (len(username.strip().split(" "))<2 and username.strip()!='' and (len(solved)==7 or len(solved)==9) and (Person.objects.filter(name=username.strip()).exists())==False):
                new = Person.objects.create(name=username.strip())
                new.save()
            elif(Person.objects.filter(name=username.strip()).exists()):
                return render(request, 'ranklist.html',{'add':add(),'invalid':False,'notexist':False,'exist':True,'ranklist':ranklist})  
            elif(len(username.strip().split(" "))>1 or username.strip()==''):
                return render(request, 'ranklist.html',{'add':add(),'invalid':True,'notexist':False,'exist':False,'ranklist':ranklist})    
            else:
                return render(request, 'ranklist.html',{'add':add(),'invalid':False,'notexist':True,'exist':False,'ranklist':ranklist})  
            return HttpResponseRedirect('/')
    if 'hidden_field' in request.POST:
        namef = hidden(request.POST)
        if namef.is_valid(): # if the booking_id is valid, delete it
            name = namef.cleaned_data['hidden_field']
            obj = Person.objects.filter(name=name)
            obj.delete()
            return HttpResponseRedirect('/')
                
    return render(request, 'ranklist.html',{'add':add(),'invalid':False,'notexist':False,'exist':False,'ranklist':ranklist})  