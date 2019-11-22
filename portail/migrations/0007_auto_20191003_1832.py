# Generated by Django 2.2.5 on 2019-10-03 18:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('portail', '0006_auto_20190919_2025'),
    ]

    operations = [
        migrations.CreateModel(
            name='CollapsibleContainer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titre', models.CharField(max_length=20)),
            ],
        ),
        migrations.AlterField(
            model_name='joueur',
            name='code',
            field=models.CharField(blank=True, default='', max_length=6),
        ),
        migrations.CreateModel(
            name='CollapsibleText',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titre', models.CharField(max_length=20, null=True)),
                ('collapsed', models.BooleanField(default=True)),
                ('contenu', models.TextField()),
                ('conteneur', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='portail.CollapsibleContainer')),
            ],
        ),
    ]