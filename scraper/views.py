from multiprocessing import context
from django.shortcuts import render   
import pymongo
from .models import *
from .serializers import *
from .forms import *
from pymongo import MongoClient
from .codes.scraping import scrap
from .codes.scraping import hello
from .codes.scraping import bey
from .codes.scraping import scraping


def home_view(request):
    context = {}
    context ['form'] = Scraping()
    return render(request,'home.html', context)

def loading_view(request):
   if request.method =='POST':
        form= Scraping(request.POST)
        if form.is_valid():
            return render(request,'loading.html')
    
def datatable_view(request):   
    if request.method =='POST':

        form = Scraping(request.POST)
        mylist=request.POST.get('checko')
        dropdown=request.POST.get('dropdown')
        if form.is_valid(): 
            if mylist is not None and dropdown == "mar":
                subject=form.cleaned_data['subject']
                print(subject)
                print(dropdown)
                #run python code of scraping
                hello(dropdown,mylist,subject)
                #ad the products scraped to the database
                client = pymongo.MongoClient("mongodb://localhost:27017/")
                # use variable names for db and collection reference
                db= client["db2"]
                col = db[subject]
                products = col.find()
                context = {'products' : products}
                #open datatable html and display all the data from database
                return render(request,'datatable.html', context)    

            elif mylist is not None and dropdown == "spain" :
                subject=form.cleaned_data['subject']
                print(subject)
                print(dropdown)
                #run python code of scraping
                bey(dropdown,mylist,subject)
                #ad the products scraped to the database
                client = pymongo.MongoClient("mongodb://localhost:27017/")
                # use variable names for db and collection reference
                db= client["db2"]
                col = db[subject]
                products = col.find()
                context = {'products' : products}
                #open datatable html and display all the data from database
                return render(request,'datatable.html', context)

            elif mylist is None and dropdown == "spain" :
                subject=form.cleaned_data['subject']
                print(subject)
                print(dropdown)
                #run python code of scraping
                scraping(dropdown,mylist,subject)
                #ad the products scraped to the database
                client = pymongo.MongoClient("mongodb://localhost:27017/")
                # use variable names for db and collection reference
                db= client["db2"]
                col = db[subject]
                products = col.find()
                context = {'products' : products}
                #open datatable html and display all the data from database
                return render(request,'datatable.html', context)

            else :
                subject=form.cleaned_data['subject']
                print(subject)
                print(dropdown)
                #run python code of scraping
                scrap(dropdown,mylist,subject)
                #ad the products scraped to the database
                client = pymongo.MongoClient("mongodb://localhost:27017/")
                # use variable names for db and collection reference
                db= client["db2"]
                col = db[subject]
                products = col.find()
                context = {'products' : products}    
                #open datatable html and display all the data from database
                return render(request,'datatable.html', context)
            #else :
            #subject=form.cleaned_data['subject']
            #print(subject)
            #print(dropdown)
            #scrap(dropdown,mylist,subject)
            #client=pymongo.MongoClient("mongodb://localhost:27017/")
            #db=client["db2"]
            #col=db[subject]
            #products=col.find()
            #context
    return
    
