# Generated by Django 5.1.1 on 2024-09-23 04:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('layuplist', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='code',
            field=models.CharField(max_length=400),
        ),
        migrations.AlterField(
            model_name='course',
            name='title',
            field=models.CharField(max_length=400),
        ),
    ]
