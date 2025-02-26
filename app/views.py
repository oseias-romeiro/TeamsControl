from django.views.generic import CreateView, TemplateView, UpdateView, ListView, DeleteView
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy, reverse
from django.shortcuts import redirect
from django.contrib import messages
from django.utils.text import slugify
import re

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

class AboutView(TemplateView):
    template_name = 'about.html'
    
class CreateUserView(CreateView):
    template_name = 'signup.html'
    form_class = CustomUserCreate

    def form_invalid(self, form):
        field = list(form.errors.keys())[0]
        first_error = form.errors[field][0]
        messages.add_message(self.request, messages.ERROR, f'{form.fields[field].label}: {first_error}')
        return super().form_invalid(form)
    
    def form_valid(self, form):
        user = form.save()
        print("user:", user)
        return redirect(reverse('login'))

    def get_success_url(self):
        messages.add_message(self.request, messages.SUCCESS, 'Profile created :D')
        return reverse_lazy('login')

class EditProfile(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    template_name = 'profile.html'
    fields = ['nome_completo', 'interesse', 'linkedin']
    model = CustomUser
    slug_field = 'username'
    slug_url_kwarg = 'username'

    def test_func(self):
        return self.get_object().id == self.request.user.id
    
    def handle_no_permission(self):
        messages.error(self.request, "You don't have permission to edit this profile")
        return redirect(reverse('index'))

    def get_success_url(self):
        messages.add_message(self.request, messages.SUCCESS, 'Profile edited')
        return reverse_lazy('index')

class TeamCreate(LoginRequiredMixin, CreateView):
    template_name = 'team/create.html'
    fields = ['owner', 'name', 'slug', 'focus', 'description', 'private']
    model = Team

    def form_invalid(self, form):
        field = list(form.errors.keys())[0]
        first_error = form.errors[field][0]
        messages.add_message(self.request, messages.ERROR, f'{field.capitalize()}: {first_error}')
        return super().form_invalid(form)

    def post(self, request, *args, **kwargs):
        owner = request.user
        name = request.POST.get('name')
        focus = request.POST.get('focus')
        description = request.POST.get('description')
        private = request.POST.get('private')

        slug = slugify(name)
        if(Team.objects.filter(slug=slug).exists()):
            messages.add_message(self.request, messages.ERROR, 'Team name already exists!')
            return redirect(f"/team/create")
        if not re.match(r'^(?!create$)[a-zA-Z0-9_-]+$', slug):
            messages.add_message(self.request, messages.ERROR, 'Invalid team name!')
            return redirect(f"/team/create")
        
        team = Team()
        team.owner = owner
        team.name = name
        team.slug = slug
        team.focus = focus
        team.description = description
        if(private == '1'): team.private = 1
        else: team.private = 0

        team.save()

        team.participants.add(owner)
        team.save()

        return redirect(f"/team/{owner.username}/list")

    def get_success_url(self):
        messages.add_message(self.request, messages.SUCCESS, 'Team created :D')
        return reverse_lazy('index')

class TeamView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    template_name = 'team/index.html'
    fields = ['owner', 'participants', 'invites', 'name', 'focus', 'description', 'private']
    model = Team
    slug_field = 'owner__username'
    slug_url_kwarg = 'username'

    def test_func(self):
        team = self.get_object()
        return team.owner_id == self.request.user.id

    def handle_no_permission(self):
        messages.error(self.request, "You don't have permission to edit this team")
        return redirect(reverse('index'))

    def post(self, request, *args, **kwargs):
        owner = request.POST.get('owner')
        team = Team.objects.filter(owner = owner)[0]
        
        name = request.POST.get('name')
        invites = request.POST.getlist('invites')
        participants = request.POST.getlist('participants')
        focus = request.POST.get('focus')
        description = request.POST.get('description')
        private = request.POST.get('private')

        if(owner not in participants):
            messages.add_message(self.request, messages.ERROR, 'Owner must be a participant!')
            return redirect(f"/team/{kwargs['username']}")
        if (len(participants) == 0):
            messages.add_message(self.request, messages.ERROR, 'You need to have at least one participant!')
            return redirect(f"/team/{kwargs['username']}")
        
        for invite in invites:
            team.participants.add(invite)
            team.invites.remove(invite)
        
        if(team.participants.count() != len(participants)):
            team.participants.clear()
            for participant in participants: team.participants.add(participant)

        team.name = name
        team.focus = focus
        team.description = description
        if(private == '1'): team.private = 1
        else: team.private = 0

        team.save()
        
        return redirect(f"/team/{kwargs['username']}")

    def get_success_url(self):
        messages.add_message(self.request, messages.SUCCESS, 'Team edited')
        return reverse_lazy('index')

class TeamDelete(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Team
    template_name = 'team/delete.html'
    slug_field = 'owner__username'
    slug_url_kwarg = 'username'

    def test_func(self):
        team = self.get_object()
        return team.owner_id == self.request.user.id
    
    def handle_no_permission(self):
        messages.error(self.request, "You don't have permission to delete this team")
        return redirect(reverse('index'))

    def get_success_url(self):
        messages.add_message(self.request, messages.SUCCESS, 'Team deleted!')
        return reverse_lazy('index')

class TeamJoin(LoginRequiredMixin, UpdateView):
    template_name = 'team/join.html'
    fields = ['invites']
    model = Team
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def post(self, request, *args, **kwargs):
        team = Team.objects.filter(slug=kwargs['slug'])[0]
        team.invites.add(request.user.id)
        return redirect(f"/team/{kwargs['slug']}")

    def get_success_url(self):
        messages.add_message(self.request, messages.SUCCESS, 'Invite sended!')
        return reverse_lazy('index')

class Teams(LoginRequiredMixin, ListView):
    template_name = 'team/list.html'
    model = Team
    slug_field = 'username'
    slug_url_kwarg = 'username'

    def get_queryset(self):
        user = self.request.user
        return super().get_queryset().filter(participants=user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

class TeamExit(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    template_name = 'team/exit.html'
    fields = ['participants']
    model = Team

    def test_func(self):
        team = self.get_object()
        return team.owner_id != self.request.user.id

    def handle_no_permission(self):
        messages.error(self.request, "You can't leave this team")
        return redirect(f"/teams/{self.request.user.username}")
    
    def post(self, request, *args, **kwargs):
        team = Team.objects.filter(pk=kwargs['pk'])[0]
        team.participants.remove(request.user.id)
        return redirect(f"/teams/{request.user.username}")

    def get_success_url(self):
        messages.add_message(self.request, messages.SUCCESS, 'Successful get out team!')
        return reverse_lazy('index')

class Work(LoginRequiredMixin, UserPassesTestMixin, ListView):
    template_name = 'work/index.html'
    model = Goal
    slug_field = 'team__slug'
    slug_url_kwarg = 'slug'

    def test_func(self):
        team = Team.objects.filter(slug=self.kwargs['slug'])[0]
        return team.participants.filter(pk=self.request.user.id).exists()
    
    def handle_no_permission(self):
        messages.error(self.request, "You don't have permission to see this team's goals")
        return redirect(reverse('index'))

    def post(self, request, *args, **kwargs):
        team = self.request.POST.get('team')
        title = self.request.POST.get('title')
        description = self.request.POST.get('description')
        deadline = self.request.POST.get('deadline')

        try:
            goal = Goal()
            goal.team = team
            goal.title = title
            goal.description = description
            goal.deadline = deadline
            goal.save()
        except:
            messages.add_message(self.request, messages.ERROR, 'Invalid information')
            return redirect("/work/"+str(kwargs['slug']))

        return redirect("/work/"+str(kwargs['slug']))
    
    def get_queryset(self, **kwargs):
        slug = self.kwargs['slug']
        team = Team.objects.filter(slug=slug)[0]
        return super().get_queryset().filter(team=team.pk, done=False).order_by('deadline')

    def get_context_data(self, **kwargs):
        slug = self.kwargs['slug']
        context = super().get_context_data(**kwargs)
        context['team'] = Team.objects.filter(slug=slug)[0]
        return context

class TaskDone(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        goal = Goal.objects.filter(pk=kwargs['pk'])[0]
        goal.done = True
        goal.save()
        return redirect("/work/"+kwargs['slug'])

class TaskListDone(LoginRequiredMixin, ListView):
    template_name = 'work/history.html'
    model = Goal
    slug_field = 'team__slug'
    slug_url_kwarg = 'slug'

    def get_queryset(self):
        team = Team.objects.filter(slug=self.kwargs['slug'])[0]
        return super().get_queryset().filter(team=team.pk, done=True).order_by('-date_update')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['team'] = {"slug": self.kwargs['slug']}
        return context
    
class TaskDelete(LoginRequiredMixin, UserPassesTestMixin, View):

    def get(self, request, *args, **kwargs):
        Goal.objects.filter(pk=kwargs['pk']).delete()
        return redirect(f"/work/{kwargs['slug']}/task/list/done")

class TaskRestore(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        goal = Goal.objects.filter(pk=kwargs['pk'])[0]
        goal.done = False
        goal.save()
        return redirect("/work/"+kwargs['slug'])
    
