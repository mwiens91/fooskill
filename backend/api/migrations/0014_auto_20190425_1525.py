# Generated by Django 2.2 on 2019-04-25 22:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0013_auto_20190425_1338'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='playerstatsnode',
            options={'ordering': ['-pk']},
        ),
    ]
