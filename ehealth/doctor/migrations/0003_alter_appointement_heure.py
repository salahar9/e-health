# Generated by Django 4.0.3 on 2022-05-01 05:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('doctor', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appointement',
            name='heure',
            field=models.CharField(choices=[('09h - 12h', 'Matin'), ('12h - 14h', 'Midi'), ('14h - 17h', 'Apres')], max_length=255),
        ),
    ]
