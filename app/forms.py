from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import CustomUser

# custom user
class CustomUserCreate(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('nome_completo', 'interesse', 'username')
        labels = {'username': 'Username/E-mail'}

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        user.email = self.cleaned_data["username"]
        if commit:
            user.save()
        
        return user

class CustomUserChange(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('nome_completo', 'interesse')
