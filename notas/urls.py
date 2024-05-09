from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.RegistroView.as_view(), name='registro'),    
    path('login/', views.LoginView.as_view(), name='login'),
    path('notas/', views.NotaLista.as_view(), name='nota-lista'),
    path('notas/<int:pk>/', views.NotaDetalle.as_view(), name='nota-detalle'),

]
