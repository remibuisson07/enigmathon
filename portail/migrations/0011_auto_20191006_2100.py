# Generated by Django 2.2.5 on 2019-10-06 21:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('portail', '0010_auto_20191006_2044'),
    ]

    operations = [
        migrations.RenameField(
            model_name='chapitre',
            old_name='image 500x500 px',
            new_name='illustration',
        ),
    ]