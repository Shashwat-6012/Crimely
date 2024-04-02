# Generated by Django 4.0.4 on 2024-03-09 11:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_property'),
    ]

    operations = [
        migrations.CreateModel(
            name='DocModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stoken', models.CharField(default='', max_length=50)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('vid', models.FileField(upload_to='documents/')),
            ],
        ),
    ]