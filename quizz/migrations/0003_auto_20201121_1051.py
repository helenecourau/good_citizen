# Generated by Django 3.0.7 on 2020-11-21 09:51

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ("quizz", "0002_auto_20201022_0827"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="result",
            options={"verbose_name": "Result"},
        ),
        migrations.AddField(
            model_name="result",
            name="last_date",
            field=models.DateTimeField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="result",
            name="success",
            field=models.BooleanField(default=True),
            preserve_default=False,
        ),
    ]
