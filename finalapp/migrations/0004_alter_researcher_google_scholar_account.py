# Generated by Django 4.0.4 on 2022-05-20 14:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('finalapp', '0003_researcher_affecte'),
    ]

    operations = [
        migrations.AlterField(
            model_name='researcher',
            name='google_scholar_account',
            field=models.URLField(blank=True, unique=True),
        ),
    ]
