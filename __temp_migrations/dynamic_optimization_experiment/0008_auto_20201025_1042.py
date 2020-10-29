# Generated by Django 2.2.12 on 2020-10-25 15:42

from django.db import migrations
import otree.db.models


class Migration(migrations.Migration):

    dependencies = [
        ('dynamic_optimization_experiment', '0007_player_all_inputs_made_in_calculator'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='player',
            name='cost_per_unit_this_round',
        ),
        migrations.AddField(
            model_name='player',
            name='cost_per_unit_this_period',
            field=otree.db.models.FloatField(null=True),
        ),
    ]
