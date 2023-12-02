from django.urls import path

from .views import TemplateView, CreateUserView, EditProfile, TeamCreate, IndexView, TeamView, DeleteTeam, JoinTeam, Teams, ExitTeam, Work, DeleteGoals;

urlpatterns = [
    path('', IndexView.as_view(), name = 'index'),
    # user
    path('signup/', CreateUserView.as_view(), name='signup'),
    path('teamCreate/', TeamCreate.as_view(), name='teamCreate'),
    path('profile/<int:pk>/', EditProfile.as_view(), name='profile'),
    # team
    path('team/<int:pk>/', TeamView.as_view(), name='team'),
    path('deleteTeam/<int:pk>/', DeleteTeam.as_view(), name='deleteTeam'),
    path('joinTeam/<int:pk>/', JoinTeam.as_view(), name='joinTeam'),
    path('teams/<int:pk>/', Teams.as_view(), name='teams'),
    path('teamExit/<int:pk>/', ExitTeam.as_view(), name='teamExit'),
    # work ambient
    path('work/<int:pk>/', Work.as_view(), name='work'),
    path('work/delete/<int:pk>/<slug:team>/', DeleteGoals.as_view(), name='deleteGoals'),
]

# error routes handler
handler404 = TemplateView.as_view(template_name='handler/404.html')
