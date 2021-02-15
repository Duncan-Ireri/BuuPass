from django.urls import include, path
from rest_framework_simplejwt import views as jwt_views

from . import views

urlpatterns = [
    path('', views.UserListView.as_view(), name='users'),
    path('register/', views.UserCreateAPIView.as_view(), name='user-register'),
    path('dj-rest-auth/', include('dj_rest_auth.urls')),


    path('create_ticket/', views.CreateTicket.as_view(), name='create-ticket'),
    path('validate_ticket/', views.UpdateTicketValidation.as_view(), name='ticket-validation'),
]