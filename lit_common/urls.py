from django.urls import path

from lit_common import views


app_name = 'lit_common'

urlpatterns = [
    path('', views.MainView.as_view(), name='main'),
]
