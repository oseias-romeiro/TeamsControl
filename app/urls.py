from django.urls import path

from .views import TemplateView, CreateUserView, EditProfile, TeamCreate, IndexView;

urlpatterns = [
    path('', IndexView.as_view(), name = 'index'),
    path('signup/', CreateUserView.as_view(), name = 'signup'),
    path('teamCreate/', TeamCreate.as_view(), name = 'teamCreate'),
    path('profile/<int:pk>/', EditProfile.as_view()),
    path('team/', TemplateView.as_view(template_name='team.html'), name = 'team'),
]

# error routes handler
handler404 = TemplateView.as_view(template_name='404.html')