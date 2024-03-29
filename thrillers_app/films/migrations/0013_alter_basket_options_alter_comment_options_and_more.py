# Generated by Django 4.1.7 on 2023-03-21 08:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('films', '0012_alter_basket_user'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='basket',
            options={'verbose_name': 'Избранное', 'verbose_name_plural': 'Избранное'},
        ),
        migrations.AlterModelOptions(
            name='comment',
            options={'verbose_name': 'Комментарий', 'verbose_name_plural': 'Комментарии'},
        ),
        migrations.AlterModelOptions(
            name='film',
            options={'verbose_name': 'Фильм', 'verbose_name_plural': 'Фильмы'},
        ),
        migrations.AddField(
            model_name='film',
            name='recommendation',
            field=models.BooleanField(default=True, null=True, verbose_name='Рекомендовать'),
        ),
        migrations.AlterField(
            model_name='film',
            name='country',
            field=models.ManyToManyField(blank=True, to='films.country', verbose_name='Страна'),
        ),
        migrations.AlterField(
            model_name='film',
            name='genre',
            field=models.ManyToManyField(blank=True, to='films.genre', verbose_name='Жанр'),
        ),
        migrations.AlterField(
            model_name='film',
            name='photo',
            field=models.ImageField(blank=True, upload_to='films/static/films/img/', verbose_name='Постер'),
        ),
    ]
