# Generated by Django 4.2.16 on 2024-09-20 20:20

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField(max_length=200, verbose_name='nombre')),
                ('description', models.TextField(max_length=300, verbose_name='descripción')),
                ('price', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='precio')),
                ('available', models.BooleanField(default=True, verbose_name='disponible')),
                ('photo', models.ImageField(blank=True, null=True, upload_to='logos', verbose_name='foto')),
            ],
        ),
    ]
