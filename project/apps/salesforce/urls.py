
from django.urls import path

# local
from . import views

urlpatterns = [
    path('import/data', views.data_import, name='import'),
]