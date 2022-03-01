from django.views.generic import CreateView, TemplateView, UpdateView, ListView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.contrib import messages

from app.forms import CustomUserCreate
from .models import CustomUser, Team, Goal

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
    form_class = CustomUserCreate

    def get_success_url(self):
        messages.add_message(self.request, messages.SUCCESS, 'Profile created :D')
        return reverse_lazy('login')

class EditProfile(LoginRequiredMixin, UpdateView):
    template_name = 'profile.html'
    fields = ['nome_completo', 'interesse', 'linkedin']
    model = CustomUser

    def get_success_url(self):
        messages.add_message(self.request, messages.SUCCESS, 'Profile edited')
        return reverse_lazy('index')

class TeamCreate(LoginRequiredMixin, CreateView):
    template_name = 'team/teamCreate.html'
    fields = ['owner', 'participants', 'name', 'focus', 'description', 'private']
    model = Team

    def get_success_url(self):
        messages.add_message(self.request, messages.SUCCESS, 'Team created :D')
        return reverse_lazy('index')

class TeamView(LoginRequiredMixin, UpdateView):
    template_name = 'team/team.html'
    fields = ['owner', 'participants', 'name', 'focus', 'description', 'private']
    model = Team

    def get_success_url(self):
        messages.add_message(self.request, messages.SUCCESS, 'Team edited')
        return reverse_lazy('index')

class DeleteTeam(LoginRequiredMixin, DeleteView):
    model = Team
    template_name = 'team/team_delete.html'

    def get_success_url(self):
        messages.add_message(self.request, messages.SUCCESS, 'Team deleted!')
        return reverse_lazy('index')

class JoinTeam(LoginRequiredMixin, UpdateView):
    template_name = 'team/joinTeam.html'
    fields = ['invites']
    model = Team

    def get_success_url(self):
        messages.add_message(self.request, messages.SUCCESS, 'Invite sended!')
        return reverse_lazy('index')

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
    fields = ['participants']
    model = Team

    def get_success_url(self):
        messages.add_message(self.request, messages.SUCCESS, 'Successful get out team!')
        return reverse_lazy('index')

class Work(LoginRequiredMixin, ListView):
    template_name = 'work/index.html'
    model = Goal

    def post(self, request, *args, **kwargs):
        team = self.request.POST.get('team')
        title = self.request.POST.get('title')
        text = self.request.POST.get('goal')

        goal = Goal()
        goal.team = team
        goal.title = title
        goal.goal = text
        goal.save()

        return redirect("/work/"+str(kwargs['pk']))
    
    def get_queryset(self, **kwargs):
        team = self.kwargs['pk']
        return super().get_queryset().filter(team=team)

    def get_context_data(self, **kwargs):
        team = self.kwargs['pk']
        context = super().get_context_data(**kwargs)
        context['team'] = Team.objects.filter(pk=team)[0]
        return context

class DeleteGoals(LoginRequiredMixin, DeleteView):
    model = Goal
    template_name = 'work/goal_delete.html'

    def post(self, request, *args, **kwargs):
        Goal.objects.filter(pk=kwargs['pk']).delete()
        return redirect("/work/"+str(kwargs['team']))