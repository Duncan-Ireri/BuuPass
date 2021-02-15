from django.urls import include, path

urlpatterns = [
    path('users/', include('authuser.urls')),
    path('tickets/', include('tickets.urls'))
]