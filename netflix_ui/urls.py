from django.urls import path
from . import views

urlpatterns = [
    path('index/', views.index, name='index'),
    path('login/', views.registration_view, name='login'),
    path('test/', views.test_backend, name='test'),
    path('error/<int:error_code>/<str:error_msg>', views.error_view, name='error'),
]