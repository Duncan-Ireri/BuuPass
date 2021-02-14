from django.urls import include, path
from rest_framework_simplejwt import views as jwt_views

from . import views

urlpatterns = [
    path('', views.UserListView.as_view(), name='users'),
    # path('token/obtain/', jwt_views.TokenObtainPairView.as_view(), name='token_create'),
    # path('token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    # path('register/', views.AuthUserCreateView.as_view(), name='register'),
    # path('login/', views.AuthUserLoginView.as_view(), name='login'),
    path('dj-rest-auth/', include('dj_rest_auth.urls')),
    path('dj-rest-auth/registration/', include('dj_rest_auth.registration.urls')),
]