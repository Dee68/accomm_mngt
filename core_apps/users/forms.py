from django import forms
from django.contrib.auth import forms as admin_forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserChangeForm as BaseUserChangeForm


User = get_user_model()

class UserChangeForm(BaseUserChangeForm):
    class Meta(BaseUserChangeForm.Meta):
        model = User
        fields = ["first_name","last_name","username","email"]


class UserCreationForm(admin_forms.UserChangeForm):
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Confirm Password", widget=forms.PasswordInput)
    class Meta(admin_forms.UserChangeForm.Meta):
        model = User
        fields = ["first_name","last_name","username","email"]
    
    error_messages = {
        "duplicate_username": "A user with that username already exists.",
        "duplicate_email": " A user with that email already exists."
    }

    def clean_email(self)->str:
        email = self.cleaned_data["email"]
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError(self.error_messages["duplicate_email"])
        return email
        

    def clean_username(self)->str:
        username = self.cleaned_data["username"]
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError(self.error_messages["duplicate_username"])
        return username
    
    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords do not match")
        return password2