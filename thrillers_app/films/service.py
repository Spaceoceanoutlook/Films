from .models import Film, Country
default_genre = None


def service_index():
    global default_genre
    default_genre = None
    films = Film.objects.all().order_by('-id')
    return films


def service_analytics():
    films = Film.objects.all()
    countries = Country.objects.all()
    analytics_country = []
    all_rating = 0
    for country in countries:
        num_country = Country.objects.get(pk=country.pk)
        how_many_countries = Film.objects.filter(country=num_country)
        res = 100 * len(how_many_countries) / len(films)
        data_country = (round(res, 2), country.title, len(how_many_countries))
        analytics_country.append(data_country)
    for film in films:
        all_rating += film.rating
    middle_rating = round((all_rating / len(films)), 2)
    analytics_country = sorted(analytics_country, reverse=True)
    return middle_rating, analytics_country, len(films)


def service_year():
    films = Film.objects.all()
    count_year = {}
    for film in films:
        if film.year not in count_year:
            count_year[film.year] = 1
        else:
            count_year[film.year] += 1
    sort_dict = dict(sorted(count_year.items(), key=lambda item: item[1], reverse=True))
    return sort_dict
