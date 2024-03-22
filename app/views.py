from django.shortcuts import render
from app.forms import *
from django.http import HttpResponse,HttpResponseRedirect
from django.core.mail import send_mail
from django.contrib.auth import authenticate,login,logout
from django.urls import reverse
from django.contrib.auth.decorators import login_required

# Create your views here.
def registration(request):
    ufo=UserForm()
    pfo=ProfileForm()
    d={'ufo':ufo,'pfo':pfo}
    if request.method=='POST' and request.FILES:
        ufd=UserForm(request.POST) #userform has only data ...so post method will get activated
        pfd=ProfileForm(request.POST,request.FILES) #profileform has both data and files  ...so in that post method will get activated and request.FILES.
        if ufd.is_valid() and pfd.is_valid():  #after validation we need to modify so that
            MUFDO=ufd.save(commit=False) # we take commit=False bcz ufo(userform object) is non modify object we need to modify the object.
            pw=ufd.cleaned_data['password'] #we need to take password colmn from ufd so we r using cleaned_data ...and all the data will be stored in one variable ...pw
            MUFDO.set_password(pw)  #set_password means oneway hashing
            MUFDO.save()
            MPFDO=pfd.save(commit=False)
            MPFDO.username=MUFDO  #in profileform we have 3 columns but we represent 2 columns in forms.so that we need take username from user..user details are in modify user from data object(MUFDO).
            MPFDO.save()
            send_mail('Registration','Thank you sooooooooo much for registration.Your registration is successful',
                      'chethanasree456@gmail.com',[MUFDO.email],fail_silently=False)
            #send_mail('subject','message','from_mail_id',['reciever_email'],fail_silently=True or False)
            return HttpResponse('registration is successfully')
        else:
            return HttpResponse('Invalid data')
    return render(request,'registration.html',d)




def home(request):
    if request.session.get('username'):
        username=request.session.get('username')
        d={'username':username}
        return render(request,'home.html',d)
    return render(request,'home.html')




def user_login(request):
    if request.method=='POST':
        username=request.POST['un']
        password=request.POST['pw']
        AUO=authenticate(username=username,password=password)  #AUO(authenticate user object)
        if AUO and AUO.is_active:          #is_active is a variable
            login(request,AUO)
            request.session['username']=username
            return HttpResponseRedirect(reverse('home'))
        else:
            return HttpResponse('username or  password are not avaliable in database')
    return render(request,'user_login.html')



@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('home'))


@login_required
def profile_display(request):
    un=request.session.get('username')
    UO=User.objects.get(username=un)
    PO=Profile.objects.get(username=UO)
    d={'UO':UO, 'PO':PO}
    return render(request,'profile_display.html',d)


@login_required
def change_password(request):
    if request.method=='POST':
        pw=request.POST['pw']
        un=request.session.get('username') 
        UO=User.objects.get(username=un)
        UO.set_password(pw)
        UO.save()
        return HttpResponse('password changed successfully')
    return render(request,'change_password.html')


def reset_password(request):
    if request.method=='POST':
        un=request.POST['un']
        pw=request.POST['pw']
        #UO=User.objects.get(username=un)
        LUO=User.objects.filter(username=un)
        if LUO:
            UO=LUO[0]
            UO.set_password(pw)
            UO.save()
            return HttpResponse('reset password changed successfully')
        else:
            return HttpResponse('Ivalid Username')
        
    return render(request,'reset_password.html')
