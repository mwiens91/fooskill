# Generated by Django 2.2 on 2019-05-03 22:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0021_playerratingnode_is_active'),
    ]

    operations = [
        migrations.AlterField(
            model_name='matchupstatsnode',
            name='game',
            field=models.ForeignKey(help_text="The game which updated the matchup's stats.", on_delete=django.db.models.deletion.CASCADE, to='api.Game'),
        ),
        migrations.AlterField(
            model_name='playerstatsnode',
            name='game',
            field=models.ForeignKey(help_text="The game which updated the player's stats.", on_delete=django.db.models.deletion.CASCADE, to='api.Game'),
        ),
    ]
