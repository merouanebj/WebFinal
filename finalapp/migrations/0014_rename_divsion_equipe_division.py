# Generated by Django 4.0.4 on 2022-05-26 18:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('finalapp', '0013_remove_equipe_laboratoire_remove_researcher_role_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='equipe',
            old_name='divsion',
            new_name='division',
        ),
    ]
