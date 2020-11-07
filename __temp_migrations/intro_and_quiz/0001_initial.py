# Generated by Django 2.2.12 on 2020-10-24 15:04

from django.db import migrations, models
import django.db.models.deletion
import otree.db.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('otree', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_in_subsession', otree.db.models.PositiveIntegerField(db_index=True, null=True)),
                ('round_number', otree.db.models.PositiveIntegerField(db_index=True, null=True)),
                ('session', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='intro_and_quiz_group', to='otree.Session')),
            ],
            options={
                'db_table': 'intro_and_quiz_group',
            },
        ),
        migrations.CreateModel(
            name='Subsession',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('round_number', otree.db.models.PositiveIntegerField(db_index=True, null=True)),
                ('session', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='intro_and_quiz_subsession', to='otree.Session')),
            ],
            options={
                'db_table': 'intro_and_quiz_subsession',
            },
        ),
        migrations.CreateModel(
            name='Player',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_in_group', otree.db.models.PositiveIntegerField(db_index=True, null=True)),
                ('_payoff', otree.db.models.CurrencyField(default=0, null=True)),
                ('round_number', otree.db.models.PositiveIntegerField(db_index=True, null=True)),
                ('_gbat_is_waiting', otree.db.models.BooleanField(choices=[(True, 'Yes'), (False, 'No')], default=False, null=True)),
                ('_gbat_grouped', otree.db.models.BooleanField(choices=[(True, 'Yes'), (False, 'No')], default=False, null=True)),
                ('income', otree.db.models.FloatField(null=True)),
                ('cost_per_unit', otree.db.models.FloatField(null=True)),
                ('experiment_sequence', otree.db.models.StringField(max_length=10000, null=True)),
                ('quiz_question_1', otree.db.models.StringField(choices=[('a', 'a'), ('b', 'b'), ('c', 'c')], max_length=10000, null=True)),
                ('quiz_question_2', otree.db.models.StringField(choices=[('true', 'true'), ('false', 'false')], max_length=10000, null=True)),
                ('group', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='intro_and_quiz.Group')),
                ('participant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='intro_and_quiz_player', to='otree.Participant')),
                ('session', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='intro_and_quiz_player', to='otree.Session')),
                ('subsession', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='intro_and_quiz.Subsession')),
            ],
            options={
                'db_table': 'intro_and_quiz_player',
            },
        ),
        migrations.AddField(
            model_name='group',
            name='subsession',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='intro_and_quiz.Subsession'),
        ),
    ]