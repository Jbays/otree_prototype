# Generated by Django 2.2.12 on 2020-10-25 00:38

from django.db import migrations
import otree.db.models


class Migration(migrations.Migration):

    dependencies = [
        ('dynamic_optimization_experiment', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='player',
            name='treatement_variable',
            field=otree.db.models.StringField(max_length=10000, null=True),
        ),
    ]
