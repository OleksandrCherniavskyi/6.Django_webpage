from django.urls import path
from . import views

urlpatterns = [

    path('', views.loginPage, name='login'),
    path('logout/', views.logoutUser, name='logout'),
    path('register/', views.registerPage, name='register'),

    path('upload', views.upload_image, name='upload_image'),
    path('images/', views.image_list, name='image_list'),
    path('magiclink/', views.magiclink, name='magiclink'),

]
