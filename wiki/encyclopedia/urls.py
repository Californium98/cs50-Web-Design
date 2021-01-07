from django.urls import path

from . import views
app_name = "encyclopedia"
urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:name>/", views.wikipage, name="wiki-page"),
    path("random/", views.random, name="random"),
    path("create/", views.create, name="create"),
    path("wiki/edit/<str:title>", views.edit, name="edit"),
    path("search/", views.search, name="search")
]
