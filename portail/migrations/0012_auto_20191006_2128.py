# Generated by Django 2.2.5 on 2019-10-06 21:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portail', '0011_auto_20191006_2100'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chapitre',
            name='illustration',
            field=models.ImageField(null=True, upload_to='illustrations'),
        ),
    ]
