from django.urls import path
from . import views

urlpatterns = [
    path("get_books/", views.get_books),
    path("get_book/<int:id>/", views.get_book),
    path("create_book/", views.create_book),
    path("update_book/<int:id>/", views.update_book),
    path("delete_book/<int:id>/", views.delete_book),
]
