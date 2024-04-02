# Generated by Django 4.0.4 on 2024-03-06 14:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Property',
            fields=[
                ('property_id', models.AutoField(primary_key=True, serialize=False)),
                ('property_name', models.CharField(max_length=100)),
                ('property_address', models.TextField()),
                ('User', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.users')),
            ],
        ),
    ]
