from django.urls import path
from app1.views import legallens,SignUpPage,main,loginpage,result,upload_file

from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('',legallens, name='home'),
    
    # path('signup/',signup,),
    path('signuppage/',SignUpPage, name='signuppage'),# data post in these path 
    path('loginpage/',loginpage, name='loginpage'),
    path('main/',main,name='main'),
    path('main/result',result,name='result'),
    #  path('analyse-document/', analyse_document, name='analyse_document')
    path('upload/',upload_file,name='upload_file'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)