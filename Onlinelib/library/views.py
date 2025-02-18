from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User,auth
from django.contrib import messages
from django.conf import settings
from .forms import Signup,Login,ContactUsForm
from django.core.mail import send_mail, BadHeaderError
from library.models import Student,books,ContactUs

def index(request):
    return render(request,'home.html')

@login_required(login_url='login')
def main(request):
    if request.method == 'POST':
        search = request.POST['search']
        Books = books.objects.filter(book_name__icontains=search)
    else:
        Books = books.objects
    return render(request,'mainPage.html', { 'Books' : Books} )    

def signup(request):
    if request.method == "POST":
        form = Signup(request.POST)
        if form.is_valid():
            firstName = form.cleaned_data["first_name"]
            lastName = form.cleaned_data["last_name"]
            email = form.cleaned_data["email_address"]
            phone = form.cleaned_data["phone"]
            password = form.cleaned_data["password"]
            username = "".join([firstName,lastName])
            if User.objects.filter(username=username).exists():
                form = Signup() 
                return render(request,"signup.html",{"form":form})
            else:
                User.objects.create_user(username=username,password=password,first_name=firstName,last_name=lastName,email=email).save()
                Student(firstName=firstName,lastName=lastName,email=email,phone=phone,password=password,).save()
                #mail
                subject = 'welcome to Online library'
                message =  f'Hi {username} thank you for registering in online library. Your id   : {username} Your pass : {password}' 
                emai_from = settings.EMAIL_HOST_USER
                recipient_mail = [email]
                send_mail(subject,message,emai_from,recipient_mail)
                return redirect("/login")
    form = Signup() 
    return render(request,"signup.html",{"form":form})    

def login(request):
    if request.method == "POST":
        form = Login(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = auth.authenticate(username=username,password=password)
            if user is not None:
                auth.login(request,user)
                return redirect("./main")
            else:
                messages.success(request,("Enter the correct username and password !"))
                return redirect("./login",{"form":form})
    else:
        form = Login()
        return render(request,"login.html",{"form":form})

def aboutus(request):
    return render(request,"aboutus.html")

def contactus(request):
    if request.method == "POST":
        form = ContactUsForm(request.POST)
        if form.is_valid():
            your_name = form.cleaned_data["your_name"]
            email_address = form.cleaned_data["email_address"]
            Your_message = form.cleaned_data["Your_message"]
            ContactUs(Your_message=Your_message,email_address=email_address,your_name=your_name).save()
            return redirect("/login")
    else:
        form = ContactUsForm()
        return render(request,"contactus.html",{"form":form})

def logout(request):
    auth.logout(request)
    return redirect('./login')
