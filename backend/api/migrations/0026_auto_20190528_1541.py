# Generated by Django 2.2 on 2019-05-28 22:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0025_auto_20190514_1945'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='player',
            options={'ordering': ['name', 'id']},
        ),
    ]
