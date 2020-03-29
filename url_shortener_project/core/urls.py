from django.urls import path
from . import views


app_name = 'core'

urlpatterns = [
    path(
        '',
        views.HomeView.as_view(),
        name='home'
    ),
    path(
        '<str:path>/',
        views.redirect_to_original,
        name='redirect_to_original'
    ),
]
