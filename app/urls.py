from django.urls import path

from .views import TemplateView;

urlpatterns = [
    path('', TemplateView.as_view(template_name='index.html'), name = 'index'),
    path('signup/', TemplateView.as_view(template_name='signup.html'), name = 'signup'),
]