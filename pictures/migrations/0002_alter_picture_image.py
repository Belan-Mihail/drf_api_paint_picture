# Generated by Django 3.2.23 on 2024-01-22 10:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pictures', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='picture',
            name='image',
            field=models.ImageField(blank=True, default='../default_post_x6zdvo', upload_to='images/'),
        ),
    ]
