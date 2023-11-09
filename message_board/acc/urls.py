from django.urls import path, include
from django.contrib.auth.views import LogoutView
from .views import Account


urlpatterns = [
    path('logout/',
         LogoutView.as_view(template_name='logout.html'),
         name='logout'),
    path('<int:pk>/', Account.as_view(success_url='/'),
         name='account'),
]
