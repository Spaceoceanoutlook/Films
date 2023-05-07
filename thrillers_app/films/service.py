from films.models import Film, Country


def service_analytics():
    films = Film.objects.all()
    country = Country.objects.all()
    analytics_country = []
    all_rating = 0
    for i in country:
        num_country = Country.objects.get(pk=i.pk)
        f = Film.objects.filter(country=num_country)
        res = len(films) / 100 * len(f)
        a = (res, i.title, len(f))
        analytics_country.append(a)
    for i in films:
        all_rating += i.rating
    middle_rating = round((all_rating / len(films)), 2)
    analytics_country = sorted(analytics_country, reverse=True)
    return middle_rating, analytics_country
