from django.urls import path
from . import views


urlpatterns = [
    path('login/', views.loginUser, name='login-page'),
    path('logout/', views.logoutUser, name='logout-user'),
    path('register/', views.registerUser, name='register-user'),



    path('', views.home, name="home"),
    # path(r'^profile/(?P<pk>[0-9a-f-]+)/$', views.profile, name="user-profile"),
    path('profile/<str:pk>/', views.profile, name="user-profile"),
    path('user-account/', views.userAccount, name="user-account"),
    
    path('edit-account/', views.editAccount, name="edit-account"),

    path('create-skill/', views.createSkill, name='create-skill'),
    path('update-skill/<str:pk>/', views.updateSkill, name='update-skill'),
    path('delete-skill/<str:pk>/', views.deleteSkill, name='delete-skill'),

    path('inbox/', views.inbox, name='inbox'),
    path('message/<str:pk>', views.viewMessages, name='view-messages'),
    path('create-message/<str:pk>', views.createMessage, name='create-message'),


]
