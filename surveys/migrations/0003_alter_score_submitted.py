# Generated by Django 3.2 on 2022-05-12 18:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('surveys', '0002_score_survey'),
    ]

    operations = [
        migrations.AlterField(
            model_name='score',
            name='submitted',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
