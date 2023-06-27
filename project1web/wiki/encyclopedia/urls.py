from django.urls import path
from . import views

app_name = "wiki"
urlpatterns = [
    path("", views.index, name="index"),    
    path("wiki/<str:title>", views.wikipage, name="wikipage"),
    path("search/", views.search, name="search"),
    path("create/", views.create_page, name="create_page"),
    path("wiki/<str:title>/edit", views.edit_page, name="edit_page"),
    path("random/", views.random_page, name="random_page")
]
