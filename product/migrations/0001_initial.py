# Generated by Django 5.0.6 on 2024-07-03 07:26

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
                ('product_name', models.CharField(max_length=200)),
                ('product_price', models.FloatField()),
                ('quantity', models.IntegerField()),
                ('description', models.TextField()),
                ('image_url', models.TextField()),
            ],
        ),
    ]
