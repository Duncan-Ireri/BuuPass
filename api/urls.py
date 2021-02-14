from django.urls import include, path

urlpatterns = [
    path('users/', include('authuser.urls')),
    # path('dj-rest-auth/', include('dj_rest_auth.urls')),
    # path('dj-rest-auth/registration/', include('dj_rest_auth.registration.urls')),
    path('tickets', include('tickets.urls'))
]