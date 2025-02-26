from django.urls import path

from .views import TemplateView, CreateUserView, EditProfile, TeamCreate, IndexView, TeamView, TeamDelete, TeamJoin, Teams, TeamExit, Work, TaskDone, AboutView, TaskListDone, TaskRestore, TaskDelete

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('about/', AboutView.as_view(), name='about'),
    # user
    path('signup/', CreateUserView.as_view(), name='signup'),
    path('profile/<slug:username>/edit', EditProfile.as_view(), name='profile_edit'),
    # team
    path('team/create/', TeamCreate.as_view(), name='team_create'),
    path('team/<slug:username>/edit', TeamView.as_view(), name='team'),
    path('team/<slug:username>/delete', TeamDelete.as_view(), name='team_delete'),
    path('team/<slug:slug>/join', TeamJoin.as_view(), name='team_join'),
    path('team/<slug:slug>/exit', TeamExit.as_view(), name='team_exit'),
    path('team/<slug:username>/list', Teams.as_view(), name='team_list'),
    # work
    path('work/<slug:slug>/', Work.as_view(), name='work'),
    path('work/<slug:slug>/task/<int:pk>/done/', TaskDone.as_view(), name='task_done'),
    path('work/<slug:slug>/task/list/done', TaskListDone.as_view(), name='task_list_done'),
    path('work/<slug:slug>/task/<int:pk>/restore/', TaskRestore.as_view(), name='task_restore'),
    path('work/<slug:slug>/task/<int:pk>/delete/', TaskDelete.as_view(), name='task_delete'),
]

# error routes handler
handler404 = TemplateView.as_view(template_name='handler/404.html')
