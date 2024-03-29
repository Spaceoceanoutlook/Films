# Generated by Django 4.1.7 on 2023-02-20 14:16

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Film',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=150)),
                ('year', models.IntegerField(blank=True)),
                ('rating', models.IntegerField(blank=True)),
                ('content', models.TextField(blank=True)),
                ('photo', models.ImageField(upload_to='media/')),
            ],
        ),
    ]
