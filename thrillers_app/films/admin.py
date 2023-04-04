from django.contrib import admin
from .models import Film, Comment, Genre, Country, Basket


class FilmAdmin(admin.ModelAdmin):
    list_display = ('title', 'year', 'rating')
    list_display_links = ('title',)
    search_fields = ('title', 'content')
    list_filter = ('genre',)
    fields = ('title', 'year', 'photo', 'genre', 'country', 'rating', 'content', 'recommendation')


admin.site.register(Film, FilmAdmin)
admin.site.register(Comment)
admin.site.register(Genre)
admin.site.register(Country)
admin.site.register(Basket)






