from django.urls import path
from skystore.apps import SkystoreConfig
from skystore.views import home, contacts

app_name = SkystoreConfig.name
urlpatterns = [
    path('',home, name='home'),
    path('contacts/',contacts, name='contacts')
]
