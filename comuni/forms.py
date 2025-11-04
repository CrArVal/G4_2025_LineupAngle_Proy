# users/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class CustomUserCreationForm(UserCreationForm):
    # Añadimos el campo de email, que no está en el UserCreationForm base
    email = forms.EmailField(
        required=True, 
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )

    class Meta(UserCreationForm.Meta):
        model = User
        # Definimos los campos que Django debe esperar
        # 'password2' ya está incluido por defecto en UserCreationForm
        fields = ('username', 'email', 'password', 'password2')

    def save(self, commit=True):
        # Guardamos el usuario
        user = super(CustomUserCreationForm, self).save(commit=False)
        # Guardamos el email que hemos añadido
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user