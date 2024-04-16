# Generated by Django 4.2.2 on 2024-04-12 13:17

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('CarDekho_app', '0011_alter_review_apiuser'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='apiuser',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
