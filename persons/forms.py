__author__ = 'shahab'
from django import forms
from .models import Home,Picture,Comment,Member,TrueFalseQuestion
from django.contrib.auth import get_user_model

User = get_user_model()

class HomeForm(forms.ModelForm):
    class Meta:
        model = Home
        fields = ['name','address', 'about','zip_code',]
    def save(self,commit=True):
        _home= super(HomeForm,self).save(commit=False)
        if commit:
            _home.save()
        return _home

class ImageForm(forms.ModelForm):
    class Meta:
        model = Picture
        fields = ['image',]
        
class CommentForm(forms.ModelForm):
    # ostan = forms.ChoiceField(choices=ostan,label="witch state",)
    class Meta:
        model = Comment
        fields = ['text']



# class TrueFalseQuestionForm(forms.ModelForm):
#     class Meta:
#         model = TrueFalseQuestion
#         fields = ('question', 'answer', )

# TrueFalseQuestionFormSet = forms.modelformset_factory(
#     TrueFalseQuestion,
#     form=TrueFalseQuestionForm,
#     extra=3
#     )



TFInlineFormSet = forms.inlineformset_factory(
    Home,
    TrueFalseQuestion,
    extra=3,
    fields=('question', 'answer'),


    )



class ArticleForm(forms.Form):
    title = forms.CharField()
    pub_date = forms.DateField()

from django.forms import formset_factory

ArticleFormSet = formset_factory(ArticleForm,extra=2)

