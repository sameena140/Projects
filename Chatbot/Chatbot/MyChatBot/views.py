from django.shortcuts import render
from django.template import RequestContext
from django.contrib import messages
import pymysql
from django.http import HttpResponse
import numpy
import tflearn
import tensorflow
import random
import json
import pickle
import nltk
from nltk.stem.lancaster import LancasterStemmer
stemmer = LancasterStemmer()
net = tflearn.input_data(shape=[None, 46])
net = tflearn.fully_connected(net, 8)
net = tflearn.fully_connected(net, 8)
net = tflearn.fully_connected(net, 6, activation="softmax")
net = tflearn.regression(net)

words = []
data = []
with open("F:/MAJOR PROJECT/Chatbot/Chatbot/MyChatBot/data.pickle", "rb") as f:
        words, labels, training, output = pickle.load(f)

with open("F:/MAJOR PROJECT/Chatbot/Chatbot/MyChatBot/dataset/question.json") as file:
    data = json.load(file)

model = tflearn.DNN(net)

model.load("F:/MAJOR PROJECT/Chatbot/Chatbot/MyChatBot/model/model.tflearn")
def bag_of_words(s, words):
    bag = [0 for _ in range(len(words))]

    s_words = nltk.word_tokenize(s)
    s_words = [stemmer.stem(word.lower()) for word in s_words]

    for se in s_words:
        for i, w in enumerate(words):
            if w == se:
                bag[i] = 1
            
    return numpy.array(bag)

def MyChatBot(request):
    if request.method == 'GET':
       return render(request, 'index.html', {})

def User(request):
    if request.method == 'GET':
       return render(request, 'User.html', {})

def Logout(request):
    if request.method == 'GET':
       return render(request, 'index.html', {})

def test(request):
    if request.method == 'GET':
       return render(request, 'test.html', {})

def Register(request):
    if request.method == 'GET':
       return render(request, 'Register.html', {})

def ChatData(request):
    if request.method == 'GET':
        question = request.GET.get('mytext', False)
        results = model.predict([bag_of_words(question, words)])
        results_index = numpy.argmax(results)
        tag = labels[results_index]
        str = "no result found"
        for tg in data["intents"]:
           if tg['tag'] == tag:
              responses = tg['responses']
              str = random.choice(responses) 
        
        print(question+" "+str)
        return HttpResponse(str, content_type="text/plain")

def UserLogin(request):
    if request.method == 'POST':
      username = request.POST.get('username', False)
      password = request.POST.get('password', False)
      index = 0
      #con = pymysql.connect("localhost","root","root","chatbot")
      con = pymysql.connect(host='127.0.0.1',port=3306,user='root',password='root',database='chatbot',charset='utf8')
      db_cursor =con.cursor()
      with con:    
          cur = con.cursor()
          cur.execute("select * FROM register")
          rows = cur.fetchall()
          for row in rows: 
             if row[0] == username and password == row[1]:
                index = 1
                break		
      if index == 1:
       context= {'data':'welcome '+username}
       return render(request, 'UserScreen.html', context)
      else:
       context= {'data':'login failed'}
       return render(request, 'User.html', context)

def Signup(request):
    if request.method == 'POST':
      username = request.POST.get('username', False)
      password = request.POST.get('password', False)
      contact = request.POST.get('contact', False)
      email = request.POST.get('email', False)
      address = request.POST.get('address', False)
      db_connection = pymysql.connect(host='127.0.0.1',port=3306,user='root',password='root',database='chatbot',charset='utf8')
      db_cursor = db_connection.cursor()
      student_sql_query = "INSERT INTO register(username,password,contact,email,address) VALUES('"+username+"','"+password+"','"+contact+"','"+email+"','"+address+"')"
      db_cursor.execute(student_sql_query)
      db_connection.commit()
      print(db_cursor.rowcount, "Record Inserted")
      if db_cursor.rowcount == 1:
       context= {'data':'Signup Process Completed'}
       return render(request, 'Register.html', context)
      else:
       context= {'data':'Error in signup process'}
       return render(request, 'Register.html', context)