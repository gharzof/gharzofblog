from django.urls import path
from .views import home, detail, add_post, about

urlpatterns = [
    path('', home, name='home'),
    path('detail/<slug:slug>/', detail, name='post_detail'),
    path('add/', add_post, name='add_post'),
    path('about/', about, name='about'),
]