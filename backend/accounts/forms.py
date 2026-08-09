from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

# Account Registration Form - email, username, password1, password2
class UserRegisterForm(UserCreationForm):
    
    email = forms.EmailField(required=True)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        
    def clean_password1(self):
        password = self.cleaned_data.get('password1')
        
        if not any(char.isupper() for char in password):
            raise forms.ValidationError("Password must contain at least one uppercase letter.")
        
        if not any(char.islower() for char in password):
            raise forms.ValidationError("Password must contain at least one lowercase letter.")

        if not any(char.isdigit() for char in password):
            raise forms.ValidationError("Password must contain at least one digit.")
        
        if not any(char.isalnum() for char in password):
            raise forms.ValidationError("Password must contain at least one special character.")
        
        return password