# Generated by Django 4.2.11 on 2024-05-17 01:35

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Token",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("user", models.CharField(max_length=100, unique=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("access_token", models.CharField(max_length=500)),
                ("refresh_token", models.CharField(max_length=500)),
                ("expires_in", models.DateTimeField()),
                ("token_type", models.CharField(max_length=100)),
            ],
        ),
    ]
