from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from app1.models import contactEnquiry
from django.contrib import messages
from django.core.mail import send_mail,EmailMultiAlternatives
import requests
from bs4 import BeautifulSoup
from apscheduler.schedulers.background import BackgroundScheduler
from django.conf import settings

# Create your views here.
url="https://academics.mnnit.ac.in/new/"

@login_required(login_url='login')
def HomePage(request):
    return render (request,'home.html')

def SignupPage(request):
    if request.method=='POST':
        uname=request.POST.get('username')
        email=request.POST.get('email')
        pass1=request.POST.get('password1')
        pass2=request.POST.get('password2')

        if pass1!=pass2:
            return HttpResponse("Your password and confrom password are not Same!!")
        else:

            my_user=User.objects.create_user(uname,email,pass1)
            my_user.save()
            return redirect('login')
        



    return render (request,'signup.html')

def LoginPage(request):
    if request.method=='POST':
        username=request.POST.get('username')
        pass1=request.POST.get('pass')
        user=authenticate(request,username=username,password=pass1)
        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            return HttpResponse ("Username or Password is incorrect!!!")

    return render (request,'login.html')

def LogoutPage(request):
    logout(request)
    return redirect('login')

def  saveEnquiry(request):
    if request.method=="POST":
        name=request.POST.get('name')
        email=request.POST.get('email')
        en=contactEnquiry(name=name,email=email)
        en.save()
        messages.success(request,"Details Added Successfully")
    return render(request, "home.html")



def find_non_common_lines(hash1, hash2):
    lines1 = set(hash1.split('\n'))
    lines2 = set(hash2.split('\n'))
    return lines1-lines2

hash1="";
hash2="";

def send_message():
    r=requests.get(url)
    htmlcontent=r.content
    # print(htmlcontent)

    soup = BeautifulSoup(htmlcontent, 'html.parser')
    panel_body = soup.find_all(class_='col-md-8', style="color:#333")

    for body in panel_body:
        global hash1
        global hash2
        hash1=hash1+"\n"+body.get_text()

    non_common_lines = find_non_common_lines(hash1, hash2)
    n=len(non_common_lines)

    if n>0:
        for line in non_common_lines:
            print(line)
            #taking out all the emails
            all_objects = contactEnquiry.objects.all()
            all_emails = [obj.email for obj in all_objects]
            recipient_list=[]

            for mails in all_emails:
                print(mails)
                recipient_list.append(mails)

            subject='New Notification'
            message=f"Heyy , we have a new notification with title {line}, for more information please visit https://academics.mnnit.ac.in/new/"
            email_from=settings.EMAIL_HOST_USER
            # recipient_list=[mails]
            send_mail(subject,message,email_from,recipient_list,fail_silently=False)
    
    hash2=hash1

def start():
    scheduler=BackgroundScheduler()
    scheduler.add_job(send_message,'interval',minutes=400)

    scheduler.start()









    # all_objects = contactEnquiry.objects.all()
# all_emails = [obj.email for obj in all_objects]
# for mails in all_emails:
#         print(mails)



# send_mail(
#     "Subject here",
#     "Here is the message.",
#     "anurag.20205040@mnnit.ac.in",
#     ["anurag.jai07@gmail.com"],
#     fail_silently=False,
# )

# subject='Testing Mail'
# form_email='anurag.20205040@mnnit.ac.in'
# msg='<p>Heyy we have new notice with title <b>ANURAG</b></p>'
# to='anurag.jai07@gmail.com'
# msg=EmailMultiAlternatives(subject,msg,form_email,[to])
# msg.content_subtype='html'
# msg.send()






#now i have a specific mail and specific line
                # subject='New Notification'
                # form_email='anurag.20205040@mnnit.ac.in'
                # msg='<p>Heyy we have new notice with title <b>ANURAG</b></p>'
                # to=mails
                # msg=EmailMultiAlternatives(subject,msg,form_email,[to])
                # msg.content_subtype='html'
                # msg.send()

                # subject='New Notification'
                # message=f"Heyy , we have a new notification with title {line}, for more information please visit https://academics.mnnit.ac.in/new/"
                # email_from=settings.EMAIL_HOST_USER
                # recipient_list=[mails]
                # send_mail(subject,message,email_from,recipient_list)
