from django.urls import path

from .views import TemplateView, CreateUserView, EditProfile, TeamCreate, IndexView, TeamView, DeleteTeam, JoinTeam;

urlpatterns = [
    path('', IndexView.as_view(), name = 'index'),
    path('signup/', CreateUserView.as_view(), name='signup'),
    path('teamCreate/', TeamCreate.as_view(), name='teamCreate'),
    path('profile/<int:pk>/', EditProfile.as_view()),
    path('team/<int:pk>/', TeamView.as_view()),
    path('deleteTeam/<int:pk>/', DeleteTeam.as_view()),
    path('joinTeam/<int:pk>/', JoinTeam.as_view()),
]

# error routes handler
handler404 = TemplateView.as_view(template_name='404.html')