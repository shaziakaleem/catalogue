from django.urls import path
from users import views
from rest_framework.authtoken.views import obtain_auth_token

# urlpatterns = [
#     path("signup/", registration_view, name="register"),
#     path("login/", obtain_auth_token, name="login"),
# ]
urlpatterns = [
    path('register/', views.register),
    path('token/', views.token),
    path('token/refresh/', views.refresh_token),
    path('token/revoke/', views.revoke_token),
]