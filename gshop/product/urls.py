from django.urls import path
from . import views 




urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login, name='login'),
    path('projects/', views.main_page, name='projects'),
    path('creation/', views.create_project, name='create_project'),
    path('<int:project_id>/chats/', views.chats, name='chats'),
    path('invites/', views.invites, name='invites'),
    path('<int:project_id>/settings/', views.project_settings, name='project_settings'),

]