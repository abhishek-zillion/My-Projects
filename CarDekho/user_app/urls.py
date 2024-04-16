from django.urls import path
from user_app import views
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('login/',obtain_auth_token,name='login'),
    path('register/',views.RegistrationView.as_view(),name='register'),
    path('logout/',views.LogoutView.as_view(),name='logout'),
]
