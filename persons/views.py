from django.shortcuts import render,redirect,get_object_or_404
from persons.models import Home,Picture,State,City,Comment,Member
from django.template import loader,RequestContext
from django.http import HttpResponse,HttpResponseRedirect
from django.forms import ModelForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .forms import HomeForm,ImageForm,CommentForm,TFInlineFormSet

from django.http import JsonResponse
from django.contrib.auth.forms import UserCreationForm
from django.views.generic.edit import CreateView
import json
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import Q
from django.forms import inlineformset_factory

from django.db.models import Count, Min, Sum, Avg

import winsound
Freq = 2500 # Set Frequency To 2500 Hertz
Dur = 1000 # Set Duration To 1000 ms == 1 second


class SignUpView(CreateView):
    template_name = 'persons/signup.html'
    form_class = UserCreationForm





def validate_username(request):
    username = request.GET.get('username', None)

    data = {
        'is_taken': User.objects.filter(username__iexact=username).exists()
    }
    if data['is_taken']:
        data['error_message'] = 'این نام کاربری قبلا ثبت نام کرده است.import'
    return JsonResponse(data)



#-------------------------------------------------------------------#
@login_required
def addHome(request):
    current_user = request.user

    template_name='persons/add_home.html'
    state = request.POST.get("state" or None)
    city = request.POST.get("city" or None)
    form1 = HomeForm(request.POST or None, request.FILES or None)
    form2 = ImageForm(request.POST or None, request.FILES or None)
    if form1.is_valid():
        if form2.is_valid():
            _home=form1.save(commit=False)
            _image=form2.save(commit=False)
            _home.member_id= current_user.id
            _home.state= state
            _home.city= city
            _home.save()
            _image.homeid= _home
            _image.save()
            current_user.member.num_homes +=1 
            current_user.member.save()
            return redirect('persons:show_homes')
    states =  State.objects.all()  

    context ={
            "form1":form1,
            "form2":form2,
            "states":states,
                    }

    return render(request,template_name,context)

def select_citys(request):
    ostan_name = request.GET.get('ostan_name'or None)
    ostan_id = State.objects.get(name=ostan_name)
    citys = City.objects.filter(ostan=ostan_id)

    a={}
    for city in citys:
        a[city.name]=city.name

    return JsonResponse(a)


#-------------------------------------------------------------------#
@login_required
def yourHomes(request):
	current_user = request.user
	#f = User.objects.filter(pk=h.member_id)

	_yourHomes= Home.objects.filter(member_id=current_user.id) 
	template_name='persons/yourHomes.html'


	return render(request,template_name,{'yourHomes':_yourHomes,'current_user':current_user})
	


#@login_required
def showHome(request):
    current_user = request.user
    template_name = 'home.html'
    homes = Home.objects.all().order_by("-timestamp")

    query = request.GET.get("q")
    if query:
        homes = homes.filter(
            Q(name__icontains = query)|
            Q(state__icontains = query)|
            Q(member__first_name__icontains = query)|
            Q(member__last_name__icontains = query)|
            Q(member__username__icontains = query)|
            Q(city__icontains = query)
        ).distinct()
	
    return render(request,template_name,{'homes':homes,'user':current_user})

def base(request):
    template_name = 'base.html'
    
    return render(request,template_name,{})

def detail_home(request,home_id):
    h = get_object_or_404(Home,id=home_id)
    f = get_object_or_404(User,pk = h.member_id)
    current_user = request.user

    im_of_this_house = Picture.objects.filter(homeid=home_id).order_by('-timestamp')
    comments = Comment.objects.filter(home=home_id).order_by('-timestamp')
    form = ImageForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        _image=form.save(commit=False)
        _image.homeid=h
        _image.save()
    form2 = CommentForm(request.POST or None)
    if form2.is_valid():
        _comment=form2.save(commit=False)
        _comment.home=h
        _comment.writer=current_user
        _comment.save()

    # context ={
    #         "home":h
    #         "owner":f
    #         "pictures":im_of_this_house
    #         "form":form
    #         "form2":form2
    #                 }
    return render(request,'persons/detail_home.html',{'home':h,'owner':f,'pictures':im_of_this_house,'form':form,'form2':form2,'comments':comments})

def detail_user(request,user_id):
    u = get_object_or_404(User,id=user_id)
    mysite ='google.com'
    context = {'u':u,'mysite':mysite}
    return render(request,'persons/detail_user.html',context)

def home_delete(request,home_id = None):
    instance = get_object_or_404(Home,id=home_id)
    current_user = request.user
    current_user.member.num_homes -=1
    current_user.member.save()
    instance.delete()
    return redirect("persons:show_homes")

def home_update(request,home_id = None):
    instance = get_object_or_404(Home,id=home_id)
    form = HomeForm(request.POST or None,instance = instance)
    # formset = TrueFalseQuestionFormSet(queryset=instance.truefalsequestion_set.all())
    formset = TFInlineFormSet()

    if request.method=="POST":
        formset = TFInlineFormSet(request.POST,queryset=instance.truefalsequestion_set.all())

        if form.is_valid() and formset.is_valid():
             # winsound.Beep(Freq,Dur)
            instance = form.save(commit=False)
            instance.save()
            tfqs = formset.save(commit = False)
            for tfq in tfqs:
                tfq.home = instance
                tfq.save()
            return HttpResponseRedirect(instance.get_absolute_url())

    context = {
            "instance": instance,
            "form":form,
            "formset":formset,
         
        }
    template_name = 'persons/home_update.html'
    return render(request, template_name, context)
def delete_image(request,img_id = None):
    img = get_object_or_404(Picture,id=img_id)
    p = img.homeid
    img.delete()
    return HttpResponseRedirect(img.get_absolute_url())
# querys
from django.db import connection
def query(request):
    q1 = User.objects.all()



    q2 = User.objects.filter(username='shab1')

    q3= Home.objects.filter(
                Q(name__icontains = "sh"))
    
    q4 = User.objects.filter(username='shab1').values('username')

    context ={
    'q1':q1.query,
    'q2':q2.query,
    'q3':q3.query,
    'q4':q4.query,
    }

    template_name= 'persons/query.html'
    return render(request,template_name,context)




# formset
# i write this method because i wanted to have a  function for formset
from . import forms
import datetime
def formset_view(request):
    formset = forms.ArticleFormSet(initial=[
     {'title': 'Django is now open source',
      'pub_date': datetime.date.today(),}
            ])
    # formset = forms.ArticleFormSet()

    if request.method == 'POST':
        formset = forms.ArticleFormSet(request.POST)
        if formset.is_valid():
            messages.success(request, "Successfully recived. Welcome Back!")
        else:
            return HttpResponse(formset.errors)
            # return HttpResponse(formset.total_error_count())
    template_name = 'persons/formset.html'
    context = {
    'formset':formset,
    }
    return render(request, template_name,context)