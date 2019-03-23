# login/views.py

from django.shortcuts import render, redirect
from .import models
from .forms import UserForm, RegisterForm, ForgetForm, ResetForm
import hashlib
from django.shortcuts import render,redirect
# from django.http import HttpResponse
# from .models import UserProfile
# from django.contrib.auth.hashers import make_password
# from apps.utils.email_send import send_register_email
# from .models import EmailVerifyRecord

def index(request):
    pass
    return render(request, 'login/index.html')


def login(request):
    if request.session.get('is_login', None):
        return redirect('/index')

    if request.method == "POST":
        login_form = UserForm(request.POST)
        message = "Please check input content！"
        if login_form.is_valid():
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']
            try:
                user = models.User.objects.get(name=username)
                if user.password == hash_code(password):  # Hash code compared with database
                    request.session['is_login'] = True
                    request.session['user_id'] = user.id
                    request.session['user_name'] = user.name
                    return redirect('/index/')
                else:
                    message = "Incorrect password！"
            except:
                message = "User doesn't exist！"
        return render(request, 'login/login.html', locals())

    login_form = UserForm()
    return render(request, 'login/login.html', locals())


def register(request):
    if request.session.get('is_login', None):
        # In login page you shouldn't register
        return redirect("/index/")
    if request.method == "POST":
        register_form = RegisterForm(request.POST)
        message = "Please check input content！"
        if register_form.is_valid():  # Obtain data
            username = register_form.cleaned_data['username']
            password1 = register_form.cleaned_data['password1']
            password2 = register_form.cleaned_data['password2']
            email = register_form.cleaned_data['email']
            sex = register_form.cleaned_data['sex']
            if password1 != password2:  # Check if two input are the same
                message = "Not the same password！"
                return render(request, 'login/register.html', locals())
            else:
                same_name_user = models.User.objects.filter(name=username)
                if same_name_user:  # User name not duplicate
                    message = 'Username exists, please input again！'
                    return render(request, 'login/register.html', locals())
                same_email_user = models.User.objects.filter(email=email)
                if same_email_user:  # E-mail address not duplicate
                    message = 'This E-mail was used, please input again！'
                    return render(request, 'login/register.html', locals())

                # Create new user

                new_user = models.User.objects.create()
                new_user.name = username
                new_user.password = hash_code(password1)  # Use hash code for password
                new_user.email = email
                new_user.sex = sex
                new_user.save()
                return redirect('/login/')  # Reload to login page
    register_form = RegisterForm()
    return render(request, 'login/register.html', locals())


# class ForgetPwdView(View):
#
#     def get(self,request):
#         forget_form=ForgetForm()
#         return render(request,'forget.html',{'forget_form':forget_form})
#     def post(self,request):
#         forget_form = ForgetForm(request.POST)
#         if forget_form.is_valid():
#             email=request.POST.get('email','')
#             send_register_email(email,'forget')
#             return render(request,'send_success.html')
#         else:
#             return render(request,'forget.html',{'forget_form':forget_form})
#
#
#
# class ResetView(View):
#
#     def get(self,request,active_code):
#         record=EmailVerifyRecord.objects.filter(code=active_code)
#         print(record)
#         if record:
#             for i in record:
#                 email=i.email
#                 is_register=UserProfile.objects.filter(email=email)
#                 if is_register:
#                     return render(request,'pwd_reset.html',{'email':email})
#         return redirect('index')
#
#
#

# class ModifyView(View):
#
#     def post(self,request):
#         reset_form=ResetForm(request.POST)
#         if reset_form.is_valid():
#             pwd1=request.POST.get('newpwd1','')
#             pwd2=request.POST.get('newpwd2','')
#             email=request.POST.get('email','')
#             if pwd1!=pwd2:
#                 return render(request,'pwd_reset.html',{'msg':'密码不一致！'})
#             else:
#                 user=UserProfile.objects.get(email=email)
#                 user.password=make_password(pwd2)
#                 user.save()
#                 return redirect('index')
#         else:
#             email=request.POST.get('email','')
#             return render(request,'pwd_reset.html',{'msg':reset_form.errors})
def logout(request):
    if not request.session.get('is_login', None):

        return redirect("/index/")
    request.session.flush()

    # del request.session['is_login']
    # del request.session['user_id']
    # del request.session['user_name']
    return redirect("/index/")

def hash_code(s, salt='mysite'):
    h = hashlib.sha256()
    s += salt
    h.update(s.encode())
    return h.hexdigest()