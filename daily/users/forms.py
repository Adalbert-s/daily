# users/forms.py
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm

class BootstrapAuthenticationForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'})
    )

class CustomUserCreationForm(forms.ModelForm):
    class Meta:
        model = get_user_model()  # Garante que o modelo CustomUser seja utilizado
        fields = ('username', 'email', 'password')  # Campos que você deseja no formulário
    
    password = forms.CharField(widget=forms.PasswordInput())  # Campo de senha
    
    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.set_password(self.cleaned_data["password"])  # Define a senha de forma segura
            user.save()
        return user
