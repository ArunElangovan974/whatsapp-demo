# Generated by Django 5.1.2 on 2025-02-24 18:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='message',
            options={},
        ),
        migrations.RenameField(
            model_name='message',
            old_name='content',
            new_name='text',
        ),
    ]
