# Generated by Django 5.0.4 on 2024-05-12 12:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0008_rename_tags_tag'),
    ]

    operations = [
        migrations.RenameField(
            model_name='tag',
            old_name='name',
            new_name='book',
        ),
        migrations.AddField(
            model_name='tag',
            name='tag_type',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]