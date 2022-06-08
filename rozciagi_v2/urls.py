from django.urls import path
from .views import wszystkie_wpisy, login_request, logout_request, nowy_wpis, filtrowanie

urlpatterns = [
    path('', nowy_wpis, name='home'),
    path('wszystkie/', wszystkie_wpisy, name='wszystkie_wpisy'),
    path('eksport/', filtrowanie, name='eksport_danych'),
    path('login/', login_request, name='login'),
    path('logout/', logout_request, name='logout'),
]