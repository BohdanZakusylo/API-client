from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('index/', views.index, name='index'),
    path('login/', views.registration_view, name='login'),
    path('test/', views.test_backend, name='test'),
    path('error/<int:error_code>/<str:error_msg>', views.error_view, name='error'),
    path('statistics/', views.pie_chart_view, name='stats'),
    path('registration-info/', views.generate_column_chart, name='registration_info'),
]