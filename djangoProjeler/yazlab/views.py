# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from bs4 import BeautifulSoup
import requests
from django.http import HttpResponse
import operator
import pymongo
from pymongo import MongoClient
from pymongo import collection
import requests


def index(request):
    if request.method=='GET':
        return render(request,'proje/input.html')
    if request.method=='POST':
        headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36 OPR/78.0.4093.184'}
        url1=request.POST.get('message')
        
        
        
        response=requests.get(url1,headers=headers)
        soup=BeautifulSoup(response.content,'lxml')

        cluster=MongoClient("mongodb+srv://baha:1234@cluster0.9l9l3.mongodb.net/test",tls=True)

        mydb = cluster["proje"]
        mycol = mydb["product"]
        
        for item in soup.select('.listing-page-content'):
            try:
                mydict = {   
                    "name": item.select('h2')[0].get_text().strip(), 
			        "price": item.select('.currency-value')[0].get_text().strip(),
			        "image-src": item.select('img')[0]['src']
  		        }
                temp_name=item.select('h2')[0].get_text().strip()
                mycol.insert_one(mydict)
            except Exception as e:
                #raise e
                b=0
        data=[]
        for item in mycol.find({'name' : temp_name},{"_id":0,"name":1,"price":1,"image-src":1}):
            
            data.append(item)
        
        return render(request,'proje/product.html',{'data':data})
