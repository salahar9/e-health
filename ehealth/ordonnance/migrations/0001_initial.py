# Generated by Django 4.0.3 on 2022-04-14 12:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('pharmacie', '__first__'),
        ('doctor', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Medicament',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Ordonnance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('le_type', models.CharField(choices=[('Traitement', 'Traitement'), ('Medicaments', 'Medicaments')], max_length=13)),
                ('duree_de_traitement', models.IntegerField()),
                ('description_de_traitement', models.CharField(max_length=255)),
                ('price', models.IntegerField(null=True)),
                ('a_mutuelle', models.BooleanField()),
                ('id_medicament', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ordonnance.medicament')),
                ('id_pharmacie', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pharmacie.pharmacie')),
                ('id_visite', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='doctor.visite')),
            ],
        ),
    ]
