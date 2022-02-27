from django.views.generic import CreateView, TemplateView, UpdateView, ListView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.shortcuts import redirect

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

class Work(LoginRequiredMixin, ListView):
    template_name = 'work/index.html'
    model = Goal

    """
    def get_queryset(self):
        teamCliente = self.request.GET.get('pk')
        return super().get_queryset().exclude(team=teamCliente)
    """
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['team'] = Team.objects.filter(owner_id=self.request.user)[0]
        return context

    def post(self, *args, **kwargs):

        data = self.request.POST

        team = Team.objects.filter(owner_id=data.get('team'))[0]

        goal = Goal()
        goal.team = team
        goal.title = data.get('title')
        goal.goal = data.get('goal')
        goal.save()

        return redirect('/work/'+data.get('team'))

class DeleteGoals(LoginRequiredMixin, DeleteView):
    model = Goal
    template_name = 'work/goal_delete.html'
    
    def get_success_url(self, **kwargs):
        goal = Goal.objects.filter(pk=self.request.POST.get('team'))[0]
        if  kwargs != None:
            return '/work/'+ goal.team_id +'/' # nao tem time: str(self.request.user.id)
        else:
            return reverse_lazy('index')