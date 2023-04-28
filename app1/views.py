from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


email_id = ""
senders_name = ""
use_name = ""


# Create your views here.
@login_required(login_url='login')
def HomePage(request):
    print(email_id)
    return render(request, 'index.html')


def SignupPage(request):
    if request.method == 'POST':
        uname = request.POST.get('username')
        email = request.POST.get('email')
        pass1 = request.POST.get('password1')
        pass2 = request.POST.get('password2')

        if pass1 != pass2:
            return HttpResponse("Your password and conform password are not Same!!")
        else:

            my_user = User.objects.create_user(uname, email, pass1)
            my_user.save()
            return redirect('login')

    return render(request, 'signup.html')


def LoginPage(request):
    global email_id, senders_name,use_name
    if request.method == 'POST':
        username = request.POST.get('username')
        pass1 = request.POST.get('pass')
        user = authenticate(request, username=username, password=pass1)
        use_name = username
        if user is not None:
            if user.is_active:
                request.session.set_expiry(86400)  # sets the exp. value of the session
                login(request, user)
                my_user = User.objects.filter(username__exact=username).values("email")
                email_id = my_user[0]["email"]
                print(email_id)
                
                return redirect('home')
    

        else:
            return HttpResponse("Username or Password is incorrect!!!")

    return render(request, 'login.html')


def LogoutPage(request):
    logout(request)
    return redirect('login')


def rms():
    return use_name

