from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from films.forms import CommentForm, UserRegForm, UserLoginForm
from films.models import Film, Comment, Genre, Country, Basket
from django.contrib import messages
from django.contrib.auth import login, logout


gp = None


def index(request):
    global gp
    gp = None
    films = Film.objects.filter(recommendation=True).order_by('-id')
    films = search(request, films)
    paginator = Paginator(films, 6)
    page_num = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_num)
    title = 'Фильмы и сериалы'
    context = {'page_obj': page_obj, 'films': films, 'title': title}
    return render(request, 'films/index.html', context=context)


def film_detail(request, film_pk):
    film = get_object_or_404(Film, pk=film_pk)
    comment = Comment.objects.filter(film=film)
    genre = Genre.objects.filter(film=film_pk)
    country = Country.objects.filter(film=film_pk)
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
    context = {'film': film, 'comment': comment, 'genre': genre, 'country': country, 'form': form, 'title': title}
    return render(request, 'films/film_detail.html', context=context)


def film_genre(request, genre_pk):
    global gp
    gp = genre_pk
    films = Film.objects.filter(genre=genre_pk).filter(recommendation=True).order_by('-id')
    genre = Genre.objects.get(pk=gp)
    title = 'Фильмы и сериалы'
    films = search(request, films)
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
    global gp
    gp = 'serials'
    title = 'Сериалы'
    films = Film.objects.filter(title__icontains='Сериал').filter(recommendation=True).order_by('-id')
    films = search(request, films)
    genre = 'Сериалы'
    paginator = Paginator(films, 6)
    page_num = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_num)
    context = {'page_obj': page_obj, 'films': films, 'title': title, 'genre': genre}
    return render(request, 'films/index.html', context=context)


def sort_by_rating(request, ascending):
    global gp
    if ascending == 1:
        if gp is None:
            films = Film.objects.filter(recommendation=True).order_by('rating')
            genre = Genre.objects.get(pk=gp)
        elif gp == 'serials':
            films = Film.objects.filter(title__icontains='Сериал').filter(recommendation=True).order_by('rating')
            genre = 'Сериалы'
        elif gp == 'not_like':
            films = Film.objects.filter(recommendation=False).order_by('rating')
            genre = 'Не понравилось'
        else:
            films = Film.objects.filter(recommendation=True).filter(genre=gp).order_by('rating')
            genre = Genre.objects.get(pk=gp)
    else:
        if gp is None:
            films = Film.objects.filter(recommendation=True).order_by('-rating')
            genre = Genre.objects.get(pk=gp)
        elif gp == 'serials':
            films = Film.objects.filter(title__icontains='Сериал').filter(recommendation=True).order_by('-rating')
            genre = 'Сериалы'
        elif gp == 'not_like':
            films = Film.objects.filter(recommendation=False).order_by('-rating')
            genre = 'Не понравилось'
        else:
            films = Film.objects.filter(recommendation=True).filter(genre=gp).order_by('-rating')
            genre = Genre.objects.get(pk=gp)
    films = search(request, films)
    title = 'Фильмы и сериалы'
    paginator = Paginator(films, 6)
    page_num = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_num)
    context = {'page_obj': page_obj, 'films': films, 'title': title, 'genre': genre}
    return render(request, 'films/index.html', context=context)


def sort_by_year(request, ascending):
    global gp
    if ascending == 1:
        if gp is None:
            films = Film.objects.filter(recommendation=True).order_by('year')
            genre = Genre.objects.get(pk=gp)
        elif gp == 'serials':
            films = Film.objects.filter(title__icontains='Сериал').filter(recommendation=True).order_by('year')
            genre = 'Сериалы'
        elif gp == 'not_like':
            films = Film.objects.filter(recommendation=False).order_by('year')
            genre = 'Не понравилось'
        else:
            films = Film.objects.filter(recommendation=True).filter(genre=gp).order_by('year')
            genre = Genre.objects.get(pk=gp)
    else:
        if gp is None:
            films = Film.objects.filter(recommendation=True).order_by('-year')
            genre = Genre.objects.get(pk=gp)
        elif gp == 'serials':
            films = Film.objects.filter(title__icontains='Сериал').filter(recommendation=True).order_by('-year')
            genre = 'Сериалы'
        elif gp == 'not_like':
            films = Film.objects.filter(recommendation=False).order_by('-year')
            genre = 'Не понравилось'
        else:
            films = Film.objects.filter(recommendation=True).filter(genre=gp).order_by('-year')
            genre = Genre.objects.get(pk=gp)
    films = search(request, films)
    title = 'Фильмы и сериалы'
    paginator = Paginator(films, 6)
    page_num = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_num)
    context = {'page_obj': page_obj, 'films': films, 'title': title, 'genre': genre}
    return render(request, 'films/index.html', context=context)


def random_film(request):
    film = Film.objects.filter(recommendation=True).order_by('?').first()
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.author = request.user
            new_comment.film = film
            new_comment.save()
    return redirect('film-info', film_pk=film.pk)


def show_not_like(request):
    global gp
    gp = 'not_like'
    films = Film.objects.filter(recommendation=False).order_by('-id')
    films = search(request, films)
    title = 'Не понравилось'
    genre = 'Не понравилось'
    paginator = Paginator(films, 6)
    page_num = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_num)
    context = {'page_obj': page_obj, 'films': films, 'title': title, 'genre': genre}
    return render(request, 'films/index.html', context=context)


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


def search(request, films):
    if request.method == 'POST':
        user_search = request.POST.get('user_search')
        for i in Film.objects.all():
            if i.title.lower() == user_search.lower() or user_search.lower() in i.title.lower():
                films = Film.objects.filter(title__icontains=f'{i.title}')
                break
        else:
            films = Film.objects.none()
    return films
