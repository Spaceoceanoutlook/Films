from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from films.forms import CommentForm, UserRegForm, UserLoginForm
from films.models import Film, Comment, Genre, Basket, Country
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from films.service import service_analytics

default_genre = None


def index(request):
    global default_genre
    default_genre = None
    films = Film.objects.all().order_by('-id')
    paginator = Paginator(films, 6)
    page_num = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_num)
    title = 'Фильмы и сериалы'
    context = {'page_obj': page_obj, 'films': films, 'title': title}
    return render(request, 'films/index.html', context=context)


def film_detail(request, film_pk):
    film = get_object_or_404(Film, pk=film_pk)
    comment = Comment.objects.filter(film=film)
    title = film.title
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.author = request.user
            new_comment.film = film
            new_comment.save()
            return redirect('film-info', film_pk=film.pk)
    else:
        form = CommentForm()
    context = {'film': film, 'comment': comment, 'form': form, 'title': title}
    return render(request, 'films/film_detail.html', context=context)


def film_genre(request, genre_pk):
    global default_genre
    default_genre = genre_pk
    films = Film.objects.filter(genre=genre_pk).order_by('-id')
    genre = Genre.objects.get(pk=default_genre)
    title = 'Фильмы и сериалы'
    paginator = Paginator(films, 6)
    page_num = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_num)
    context = {'page_obj': page_obj, 'films': films, 'title': title, 'genre': genre}
    return render(request, 'films/index.html', context=context)


# def new_film(request):
#     if request.method == "GET":
#         form = FilmForm()
#         context = {'form': form}
#         return render(request, 'films/new_film.html', context=context)
#     else:
#         form = FilmForm(request.POST, request.FILES)
#         if form.is_valid():
#             film = form.save()
#             film.save()
#             return redirect('index')


# def edit_film(request, film_pk):
#     film = get_object_or_404(Film, pk=film_pk)
#     if request.method == "GET":
#         form = FilmForm(instance=film)
#         context = {'form': form}
#         return render(request, 'films/edit_film.html', context=context)
#     else:
#         form = FilmForm(request.POST, request.FILES, instance=film)
#         if form.is_valid():
#             film = form.save()
#             film.save()
#             return redirect('film-info', film_pk=film.pk)


# def delete_film(request, film_pk):
#     if request.method == "GET":
#         film = get_object_or_404(Film, pk=film_pk)
#         film.delete()
#         return redirect('index')


def delete_comment(request, comment_pk, film_pk):
    if request.method == "GET":
        film = Film.objects.get(pk=film_pk)
        comment = get_object_or_404(Comment, pk=comment_pk)
        comment.delete()
        return redirect('film-info', film_pk=film.pk)


def add_basket(request, film_pk):
    film = Film.objects.get(pk=film_pk)
    basket = Basket.objects.filter(user=request.user).first()
    if basket is None:
        basket = Basket.objects.create(user=request.user)
    basket.films.add(film)
    return redirect('film-info', film_pk=film.pk)


def show_basket(request):
    basket = Basket.objects.filter(user=request.user).first()
    if basket is None:
        basket = Basket.objects.create(user=request.user)
    film = basket.films.all()
    title = 'Избранное'
    context = {'film': film, 'title': title}
    return render(request, 'films/basket.html', context=context)


def delete_from_basket(request, film_pk):
    basket = Basket.objects.filter(user=request.user).first()
    basket.films.remove(film_pk)
    return redirect('show_basket')


def clear_basket(request):
    basket = Basket.objects.filter(user=request.user).first()
    basket.films.clear()
    return redirect('show_basket')


def show_serials(request):
    global default_genre
    default_genre = 'serials'
    title = 'Сериалы'
    films = Film.objects.filter(title__icontains='Сериал').order_by('-id')
    genre = 'Сериалы'
    paginator = Paginator(films, 6)
    page_num = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_num)
    context = {'page_obj': page_obj, 'films': films, 'title': title, 'genre': genre}
    return render(request, 'films/index.html', context=context)


def sort_by_rating(request, ascending):
    global default_genre
    if ascending == 1:
        if default_genre is None:
            films = Film.objects.all().order_by('rating')
            genre = Genre.objects.none()
        elif default_genre == 'serials':
            films = Film.objects.filter(title__icontains='Сериал').order_by('rating')
            genre = 'Сериалы'
        elif default_genre == 'not_like':
            films = Film.objects.all().order_by('rating')
            genre = 'Не понравилось'
        elif default_genre == 'rus':
            country_1 = Country.objects.get(title='СССР')
            country_2 = Country.objects.get(title='Россия')
            films_1 = Film.objects.filter(country=country_1.pk)
            films_2 = Film.objects.filter(country=country_2.pk)
            films = (films_1 | films_2).order_by('rating')
            genre = 'Русские / советские'
        else:
            films = Film.objects.filter(genre=default_genre).order_by('rating')
            genre = Genre.objects.get(pk=default_genre)
    else:
        if default_genre is None:
            films = Film.objects.all().order_by('-rating')
            genre = Genre.objects.none()
        elif default_genre == 'serials':
            films = Film.objects.filter(title__icontains='Сериал').order_by('-rating')
            genre = 'Сериалы'
        elif default_genre == 'not_like':
            films = Film.objects.all().order_by('-rating')
            genre = 'Не понравилось'
        elif default_genre == 'rus':
            country_1 = Country.objects.get(title='СССР')
            country_2 = Country.objects.get(title='Россия')
            films_1 = Film.objects.filter(country=country_1.pk)
            films_2 = Film.objects.filter(country=country_2.pk)
            films = (films_1 | films_2).order_by('-rating')
            genre = 'Русские / советские'
        else:
            films = Film.objects.filter(genre=default_genre).order_by('-rating')
            genre = Genre.objects.get(pk=default_genre)
    title = 'Фильмы и сериалы'
    paginator = Paginator(films, 6)
    page_num = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_num)
    context = {'page_obj': page_obj, 'films': films, 'title': title, 'genre': genre}
    return render(request, 'films/index.html', context=context)


def sort_by_year(request, ascending):
    global default_genre
    if ascending == 1:
        if default_genre is None:
            films = Film.objects.all().order_by('year')
            genre = Genre.objects.none()
        elif default_genre == 'serials':
            films = Film.objects.filter(title__icontains='Сериал').order_by('year')
            genre = 'Сериалы'
        elif default_genre == 'not_like':
            films = Film.objects.all().order_by('year')
            genre = 'Не понравилось'
        elif default_genre == 'rus':
            country_1 = Country.objects.get(title='СССР')
            country_2 = Country.objects.get(title='Россия')
            films_1 = Film.objects.filter(country=country_1.pk)
            films_2 = Film.objects.filter(country=country_2.pk)
            films = (films_1 | films_2).order_by('year')
            genre = 'Русские / советские'
        else:
            films = Film.objects.filter(genre=default_genre).order_by('year')
            genre = Genre.objects.get(pk=default_genre)
    else:
        if default_genre is None:
            films = Film.objects.all().order_by('-year')
            genre = Genre.objects.none()
        elif default_genre == 'serials':
            films = Film.objects.filter(title__icontains='Сериал').order_by('-year')
            genre = 'Сериалы'
        elif default_genre == 'not_like':
            films = Film.objects.all().order_by('-year')
            genre = 'Не понравилось'
        elif default_genre == 'rus':
            country_1 = Country.objects.get(title='СССР')
            country_2 = Country.objects.get(title='Россия')
            films_1 = Film.objects.filter(country=country_1.pk)
            films_2 = Film.objects.filter(country=country_2.pk)
            films = (films_1 | films_2).order_by('-year')
            genre = 'Русские / советские'
        else:
            films = Film.objects.filter(genre=default_genre).order_by('-year')
            genre = Genre.objects.get(pk=default_genre)
    title = 'Фильмы и сериалы'
    paginator = Paginator(films, 6)
    page_num = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_num)
    context = {'page_obj': page_obj, 'films': films, 'title': title, 'genre': genre}
    return render(request, 'films/index.html', context=context)


def random_film(request):
    film = Film.objects.all().order_by('?').first()
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.author = request.user
            new_comment.film = film
            new_comment.save()
    return redirect('film-info', film_pk=film.pk)


def register(request):
    if request.method == 'POST':
        form = UserRegForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Успешная регистрация')
            return redirect('index')
        else:
            messages.error(request, 'Что-то пошло не так')
    else:
        form = UserRegForm()
    title = 'Фильмы и сериалы'
    context = {'form': form, 'title': title}
    return render(request, 'films/register.html', context=context)


def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('index')
    else:
        form = UserLoginForm()
    title = 'Авторизация'
    context = {'form': form, 'title': title}
    return render(request, 'films/login.html', context=context)


def user_logout(request):
    logout(request)
    return redirect('login')


def search(request):
    user_search = request.GET.get('search')
    if len(user_search) < 3:
        films = Film.objects.none()
    else:
        films_1 = Film.objects.filter(title__icontains=f'{user_search.lower()}')
        films_2 = Film.objects.filter(title__icontains=f'{user_search.capitalize()}')
        films = films_1.union(films_2)
        list_films = []
        for i in films:
            title_film = i.title.lower().split()
            if user_search.lower() in title_film:
                list_films.append(i.pk)
            for j in title_film:
                if j.startswith(user_search.lower()):
                    list_films.append(i.pk)
        films = Film.objects.filter(pk__in=list_films) # делаем из списка queryset
    title = 'Поиск'
    context = {'films': films, 'title': title}
    return render(request, 'films/search.html', context=context)


def my_profile(request, profile_id):
    user = User.objects.get(id=profile_id)
    comment = Comment.objects.filter(author_id=profile_id)
    title = f'{user.username}'
    context = {'comment': comment, 'title': title}
    return render(request, 'films/user_profile.html', context=context)


def only_russians(request):
    global default_genre
    default_genre = 'rus'
    country_1 = Country.objects.get(title='СССР')
    country_2 = Country.objects.get(title='Россия')
    films_1 = Film.objects.filter(country=country_1.pk)
    films_2 = Film.objects.filter(country=country_2.pk)
    films = (films_1 | films_2).order_by('-id')
    title = 'Русские / советские'
    paginator = Paginator(films, 6)
    page_num = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_num)
    context = {'page_obj': page_obj, 'films': films, 'title': title}
    return render(request, 'films/index.html', context=context)


def country_films(request, pk):
    global default_genre
    default_genre = None
    films = Film.objects.filter(country=pk).order_by('-id')
    country = Country.objects.get(pk=pk)
    title = 'Фильмы и сериалы'
    paginator = Paginator(films, 6)
    page_num = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_num)
    context = {'page_obj': page_obj, 'films': films, 'title': title, 'country': country}
    return render(request, 'films/index.html', context=context)


def analytics(request):
    middle_rating, analytics_country = service_analytics()
    context = {'analytics_country': analytics_country, 'middle_rating': middle_rating}
    return render(request, 'films/analytics.html', context=context)

