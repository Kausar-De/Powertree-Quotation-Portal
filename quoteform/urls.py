from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.loginPage, name = "login"),
    path('logout/', views.logoutUser, name = "logout"),

    path('', views.quoteForm, name = "quoteform"),
    path('quotelist/', views.quoteList, name = "quotelist"),
    path('quotedetail/<int:pk>/', views.quoteDetail, name='quotedetail'),
]