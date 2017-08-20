from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User


class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(min_length=6,
                               widget=forms.PasswordInput,
                               required=True)


class SignUpForm(UserCreationForm):

    first_name = forms.CharField(
        max_length=30,
        required=False,
        help_text='Please enter your first name'
    )
    last_name = forms.CharField(
        max_length=30,
        required=False,
        help_text='Please enter your last name'
    )
    email = forms.EmailField(max_length=254,
                             help_text='Input a valid email address')
    phone = forms.CharField(initial='+380')
    birthday = forms.DateField(widget=forms.SelectDateWidget(years=[x for x in range(1917, 2000)]))

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'phone', 'birthday', 'password1', 'password2',)

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user
