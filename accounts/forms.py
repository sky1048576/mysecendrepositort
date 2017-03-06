from django import forms
from django.contrib.auth import get_user_model
from django.forms import ModelForm, CharField
from django.core.exceptions import NON_FIELD_ERRORS
from persons.models import Member
User = get_user_model()


class ReistrationForm(ModelForm):
    username = forms.CharField(error_messages={'required': 'این فیلد ضروری است',
        'invalid':'استفاده از علائهمی مثل @# و ... امکان پذیر نیست'},
        help_text='نام کاربری وارد کن')
    password1 = forms.CharField(label="pass", widget=forms.PasswordInput())
    password2 = forms.CharField(label="pass_confirm",widget=forms.PasswordInput())
    email = forms.EmailField(
      widget=forms.EmailInput(attrs={
        'autocomplete': 'off',
        'placeholder': ('seuemail@email.com'),
        'required': 'required'
      }),
      error_messages={'invalid': 'این ایمیل معتبر نیست'}
    )

    class Meta:
        model = User
        # fields = '__all__'
        fields = ['username', 'email', ]
        help_texts = {
            'username': ('لطفا نام کاربری خود را اینجا وارد کنید'),
            'email': ('با هر ایمیل یک بار میتوان ثبت نام کرد'),
        }
     
    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("password do not match")
        return password2

    def clean_email(self):
        email = self.cleaned_data.get("email")
        user_count = User.objects.filter(email=email).count()
        print
        user_count
        if user_count > 0 and email:
            raise forms.ValidationError("this email is signed up before")
        return email

    def save(self, commit=True):
        user = super(ReistrationForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user

# takmil etelaat
from django import forms
class InformationForm(forms.Form):
    first_name = forms.CharField(label='Your name', max_length=100)
    last_name = forms.CharField(label='Your last', max_length=100)
    phone_number = forms.CharField(label='phone_number', max_length=100)
    national_code = forms.CharField(label='national_code', max_length=100)




class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name','last_name']
        
class MemberForm(forms.ModelForm):
    class Meta:
        model = Member
        fields = ['phone_number','national_code','about']
class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())

    def clean_username(self):
        username = self.cleaned_data.get("username")
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise forms.ValidationError("Are you sure you are registered? We cannot find this user.")
        return username

    def clean_password(self):
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")
        try:
            user = User.objects.get(username=username)
        except:
            user = None
        if user is not None and not user.check_password(password):
            raise forms.ValidationError("Invalid Password")
        elif user is None:
            pass
        else:
            return password
