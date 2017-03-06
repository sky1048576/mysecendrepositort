from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth import login, authenticate,logout
from .forms import ReistrationForm,InformationForm,UserForm,MemberForm,LoginForm
from django.contrib.auth.models import User
from persons.models import Member
# Create your views here.
from django.contrib import messages

from django.contrib.auth.forms import UserCreationForm
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from django.core import urlresolvers
from django.http import HttpResponseRedirect
from persons.models import Member


def register(request, ):
    form = ReistrationForm(request.POST or None)

    if form.is_valid():
        new_user = form.save(commit=False)
        # ba dastoore zir mitavan first_name ra ham az inja meghdardehi kard
        # new_user.first_name = "justi"
        new_user.save()
        new_memeber = Member()
        new_memeber.user_id = new_user.pk
        new_memeber.save()
        login(request, new_user)

        return redirect('persons:show_homes')
    context = {

        "form": form
    }
    return render(request, "registration/register.html", context)


def information(request):

    current_user = request.user
    # phone_number = request.POST.get("phone_number" or None)
    # national_code = request.POST.get("national_code" or None)
    template_name='registration/information.html'
    instance1 = get_object_or_404(User,id=current_user.id)
    try:
        instance2 = Member.objects.get(user=current_user)
    except:
        instance2 = Member.objects.create(user=current_user)
            

    form1 = UserForm(request.POST or None,instance = instance1)
    form2 = MemberForm(request.POST or None,instance = instance2)
    if form1.is_valid():
        if form2.is_valid():
            _user=form1.save(commit=False)
            _member=form2.save(commit=False)
            _user.id= current_user.id
            # _member.phone_number= phone_number
            # _member.national_code= national_code
            _member.save()
            _user.save()
            return redirect(_member)

    context ={
            "form1":form1,
            "form2":form2,
                    }

    return render(request,template_name,context)   

def login_view(request):
    form = LoginForm(request.POST or None)
    btn = "Login"
    if form.is_valid():
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = authenticate(username=username, password=password)
        login(request, user)
        messages.success(request, "Successfully Logged In. Welcome Back!")
        return redirect('persons:yourHomes')
    context = {
        "form": form,
        "submit_btn": btn,
    }
    return render(request, "registration/login.html", context)



def logout_view(request):
    logout(request)
    return HttpResponseRedirect("/")
   