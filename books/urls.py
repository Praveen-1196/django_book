from django.urls import path
from . import views

urlpatterns = [
    path("register/", views.register),
    path("login/", views.login),
    path("create_book/", views.create_book),
    path("get_books/", views.get_books),
    path("get_book/<int:id>/", views.get_book),
    path("update_book/<int:id>/", views.update_book),
    path("delete_book/<int:id>/", views.delete_book),
     path("books_page/", views.book_list_page),
]
