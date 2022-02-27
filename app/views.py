from django.views.generic import CreateView, TemplateView, UpdateView, ListView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy

from app.forms import CustomUserCreate
from .models import CustomUser, Team

class IndexView(ListView):
    template_name = 'index.html'
    model = Team

    def get_queryset(self):
        user = self.request.user
        if(not user.is_anonymous):
            return super().get_queryset().filter(private=False).exclude(participants=user)
        else:
            return super().get_queryset().filter(private=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

class CreateUserView(CreateView):
    template_name = 'signup.html'
    success_url = reverse_lazy('login')
    form_class = CustomUserCreate

class EditProfile(LoginRequiredMixin, UpdateView):
    template_name = 'profile.html'
    success_url = reverse_lazy('profile')
    fields = ['nome_completo', 'interesse', 'linkedin']
    model = CustomUser

class TeamCreate(LoginRequiredMixin, CreateView):
    template_name = 'team/teamCreate.html'
    success_url = reverse_lazy('index')
    fields = ['owner', 'participants', 'name', 'focus', 'description', 'private']
    model = Team

class TeamView(LoginRequiredMixin, UpdateView):
    template_name = 'team/team.html'
    success_url = reverse_lazy('index')
    fields = ['owner', 'participants', 'name', 'focus', 'description', 'private']
    model = Team

class DeleteTeam(LoginRequiredMixin, DeleteView):
    model = Team
    template_name = 'team/team_delete.html'
    success_url = reverse_lazy('index')

class JoinTeam(LoginRequiredMixin, UpdateView):
    template_name = 'team/joinTeam.html'
    success_url = reverse_lazy('index')
    fields = ['invites']
    model = Team

class Teams(LoginRequiredMixin, ListView):
    template_name = 'team/teams.html'
    model = Team

    def get_queryset(self):
        user = self.request.user
        return super().get_queryset().filter(participants=user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

class ExitTeam(LoginRequiredMixin, UpdateView):
    template_name = 'team/exitTeam.html'
    success_url = reverse_lazy('index')
    fields = ['participants']
    model = Team

class Work(TemplateView):
    template_name = 'work/index.html'
    