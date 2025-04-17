from django.urls import path
from app1.views import legallens,SignUpPage,main,loginpage,result,upload_file
urlpatterns = [
    path('',legallens, name='home'),
    
    # path('signup/',signup,),
    path('signuppage/',SignUpPage, name='signuppage'),# data post in these path 
    path('loginpage/',loginpage, name='loginpage'),
    path('main/',main,name='main'),
    path('main/result',result,name='result'),
    #  path('analyse-document/', analyse_document, name='analyse_document')
    path('upload/',upload_file,name='upload_file'),
]