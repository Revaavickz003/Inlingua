# Generated by Django 5.0.1 on 2024-02-13 10:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Inlingua_app', '0007_remove_paymenttypes_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='studentdetails',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(blank=True, max_length=254, verbose_name='email address'),
        ),
    ]
