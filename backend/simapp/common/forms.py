from django import forms
from django.contrib.auth import authenticate

from .models import User


class UserForm(forms.ModelForm):

    password = forms.CharField(max_length=100, required=False)

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'username']

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)

        #self.fields['first_name'].required = True
        #self.fields['username'].required = True
        self.fields['email'].required = True

        if not self.instance.pk:
            self.fields['password'].required = True

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if password:
            if len(password) < 4:
                raise forms.ValidationError(
                    'Password must be at least 4 characters long!')
        return password

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if self.instance.id:
            if self.instance.email != email:
                if not User.objects.filter(email=self.cleaned_data.get("email")).exists():
                    return self.cleaned_data.get("email")
                else:
                    raise forms.ValidationError('Email already exists')
            else:
                return self.cleaned_data.get("email")
        else:
            if not User.objects.filter(email=self.cleaned_data.get("email")).exists():
                    return self.cleaned_data.get("email")
            else:
                raise forms.ValidationError('User already exists with this email')


class LoginForm(forms.ModelForm):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['email', 'password']

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request", None)
        super(LoginForm, self).__init__(*args, **kwargs)

    def clean(self):
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")

        if email and password:
            self.user = authenticate(email=email, password=password)
            print (self.user)
            if self.user:
                if not self.user.is_active:
                    raise forms.ValidationError("User is Inactive")
            else:
                raise forms.ValidationError("Invalid email and password")
        return self.cleaned_data


class ChangePasswordForm(forms.Form):
    password1 = forms.CharField(max_length=100,label='Password')
    password2 = forms.CharField(max_length=100,label='Password confirm')


    def clean_password1(self):
        if len(self.data.get('password1')) < 8:
            raise forms.ValidationError(
                'Password must be at least 8 characters long!')
        if self.data.get('password1') != self.data.get('password2'):
            print(self.data.get('password1'))
            print(self.cleaned_data.get('password2'))
            raise forms.ValidationError(
                'Confirm password do not match with new password')
        return self.data.get('password1')