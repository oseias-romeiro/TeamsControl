from django.views.generic import CreateView, TemplateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy

from app.forms import CustomUserCreate, CustomUserChange
from .models import CustomUser

class CreateUserView(CreateView):
    template_name = 'signup.html'
    success_url = reverse_lazy('login')
    form_class = CustomUserCreate

class EditProfile(LoginRequiredMixin, UpdateView):
    template_name = 'profile.html'
    success_url = reverse_lazy('profile')
    fields = ['nome_completo', 'interesse', 'linkedin']
    model = CustomUser