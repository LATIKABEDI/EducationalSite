
from urllib.robotparser import RequestRate
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from blog.models import Post, Category,Contact
from django.contrib.auth.models import User, auth
from datetime import datetime


# Create your views here.
def home(request):
    # load all the post from db(10)
    posts = Post.objects.all()[:11]
    # print(posts)

    cats = Category.objects.all()

    data = {
        'posts': posts,
        'cats': cats
    }
    return render(request, 'home.html', data)


def post(request, url):
    post = Post.objects.get(url=url)
    cats = Category.objects.all()

    # print(post)
    return render(request, 'posts.html', {'post': post, 'cats': cats})


def category(request, url):
    cat = Category.objects.get(url=url)
    posts = Post.objects.filter(cat=cat)
    cats = Category.objects.all()
    return render(request, "category.html", {'cat': cat, 'posts': posts,'cats': cats})

def contact(request):
    check = ['select * from', 'SELECT * FROM', 'union select', 'UNION SELECT', 'select', 'union', 'SELECT', 'UNION', '"', '""', "&&", 'OR'] # checking for bad characters
    cats = Category.objects.all() #fetching categories to every page


    if request.method == "GET":
        return render(request,'contact.html',{'cats': cats})

    if request.method =="POST":
        name=request.POST.get('name')
        email=request.POST.get('email')
        message=request.POST.get('message')

        if not name or not email or not message:
            return error(request)
        elif any(x in name for x in check) or any(x in email for x in check) or any(x in message for x in check):
            return error(request)
        else:
            contact=Contact(name=name, email=email,message=message,date=datetime.today())
            contact.save()
            return render(request , 'contact.html',{'cats': cats})
     
def about(request):
    cats = Category.objects.all() #fetching categories to every page
    return render(request , 'about.html',{'cats': cats})     


def error(request):
    return render(request, 'errorPage.html')

def signup(request):
    
    
    if request.method =='POST':
        #get the paramerters
        fname=request.POST['fname']
        lname=request.POST['lname']
        email=request.POST['email']
        username=request.POST['username']
        password1=request.POST['password1']
        password2=request.POST['password2']

        #checks for errorneous inputs
        if len(username)<10:
            messages.error(request, " Your user name must not  be under 10 characters")
            return redirect('/home/')

        if not username.isalnum():
            messages.error(request, " Username should only contain letters and numbers")
            return redirect('/home/')
        if (password1 != password2):
             messages.error(request, " Passwords do not match")
             return redirect('/home/')

        #create the user
        user=User.objects.create_user(username,email,password1)
        user.first_name=fname
        user.last_name=lname 
        user.save()
        messages.success(request,"Your account has been successfully created.")
        return redirect('/home/')

    else:
        return render(request, 'signUpPage.html')
        

def search(request):
    return HttpResponse('THIS IS SEARCH PAGE')
    

def login(request):
    return render(request,'loginpage.html')