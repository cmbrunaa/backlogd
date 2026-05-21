from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('buscar/', views.buscar, name='buscar'),
    path('adicionar/', views.adicionar_game, name='adicionar_game'),
    path('editar/<int:id>/', views.editar_game, name='editar_game'),
    path('deletar/<int:id>/', views.deletar_game, name='deletar_game'),
    path('game/<int:id>/', views.detalhes_game, name='detalhes_game'),

    path('login/', views.login_usuario, name='login'),
    path('cadastro/', views.cadastro_usuario, name='cadastro'),
    path('logout/', views.logout_usuario, name='logout'),
]