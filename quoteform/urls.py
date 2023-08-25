from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.loginPage, name = "login"),
    path('logout/', views.logoutUser, name = "logout"),

    path('', views.quoteForm, name = "quoteform"),
    path('quotelist/', views.quoteList, name = "quotelist"),
    path('quotedetail/<int:pk>/', views.quoteDetail, name='quotedetail'),
    path('updatequote/<str:pk>', views.updateQuote, name = "updatequote"),
    path('showcsv/', views.showCsv, name = "showcsv"),

    path('renderpdf/<int:pk>/', views.renderPDF, name='renderpdf'),
    path('sendmail/<int:pk>/', views.sendMail, name='sendmail'),  

    path('customercare/', views.customerHome, name = "customercare"),
    path('customerform/', views.customerForm, name = "customerform"),
    path('thankyou/', views.thankYou, name='thankyou'),
]