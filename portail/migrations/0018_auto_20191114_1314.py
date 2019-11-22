# Generated by Django 2.2.5 on 2019-11-14 13:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('portail', '0017_joueur_invite'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chapitre',
            name='couleurfond',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='portail.Couleur'),
        ),
        migrations.AlterField(
            model_name='chapitre',
            name='illustration',
            field=models.ImageField(blank=True, upload_to='illustrations'),
        ),
        migrations.AlterField(
            model_name='chapitre',
            name='introduction',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='collapsibletext',
            name='titre',
            field=models.CharField(blank=True, max_length=20),
        ),
    ]