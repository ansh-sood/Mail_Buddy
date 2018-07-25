from django.conf.urls import url
from . import views

app_name = 'hab_app'
urlpatterns = [
    url(r'gmail/$', views.processRequest, name='process_request'),
]