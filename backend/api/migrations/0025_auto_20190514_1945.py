# Generated by Django 2.2 on 2019-05-15 02:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0024_auto_20190511_1303'),
    ]

    operations = [
        migrations.AlterField(
            model_name='playerratingnode',
            name='rating_volatility',
            field=models.FloatField(help_text="The player's rating volatility for this rating period. This is only used if the rating algorithm is Glicko-2.", null=True),
        ),
    ]