from django.urls import path
from .views import index, film_detail, film_genre, delete_comment, show_basket, \
    add_basket, delete_from_basket, clear_basket, show_serials, sort_by_rating, sort_by_year, random_film, \
    register, user_login, user_logout, my_profile, search, only_russians, country_films, analytics, year_films

urlpatterns = [
    path('', index, name='index'),
    path('film/<int:film_pk>/', film_detail, name='film-info'),
    # path('film/delete_film/<int:film_pk>/', delete_film, name='delete_film'),
    path('film/delete_comment/<int:film_pk>/<int:comment_pk>/', delete_comment, name='delete_comment'),
    # path('new_film/', new_film, name='new_film'),
    # path('edit_film/<int:film_pk>/', edit_film, name='edit_film'),
    path('film/genre/<int:genre_pk>/', film_genre, name='film_genre'),
    path('basket/', show_basket, name='show_basket'),
    path('add_basket/<int:film_pk>/', add_basket, name='add_basket'),
    path('delete_from_basket/<int:film_pk>/', delete_from_basket, name='delete_from_basket'),
    path('clear_basket/', clear_basket, name='clear_basket'),
    path('show_serials/', show_serials, name='show_serials'),
    path('sort_by_rating/<int:ascending>/', sort_by_rating, name='sort_by_rating'),
    path('sort_by_year/<int:ascending>/', sort_by_year, name='sort_by_year'),
    path('random_film/', random_film, name='random_film'),
    path('register/', register, name='register'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('user_profile/<int:profile_id>/', my_profile, name='my_profile'),
    path('search/', search, name='search'),
    path('only_russians/', only_russians, name='only_russians'),
    path('country_films/<int:pk>/', country_films, name='country_films'),
    path('analytics/', analytics, name='analytics'),
    path('year_films/<int:pk>/', year_films, name='year_films'),
]
