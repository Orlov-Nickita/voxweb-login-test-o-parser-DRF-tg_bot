# Generated by Django 4.2.3 on 2023-07-31 15:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductCountDownloaded',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('count', models.IntegerField(verbose_name='Количество добавленных товаров в БД')),
                ('downloaded_at', models.DateTimeField(auto_now_add=True, verbose_name='дата добавления в БД')),
            ],
            options={
                'verbose_name': 'загруженный товар',
                'verbose_name_plural': 'загруженные товары',
            },
        ),
    ]
