# Generated by Django 4.2.7 on 2023-11-27 14:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fruitshop_app', '0007_alter_message_message_data_time'),
    ]

    operations = [
        migrations.CreateModel(
            name='DownloadStatistics',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(unique=True)),
                ('quantity_of_downloads', models.PositiveIntegerField()),
            ],
        ),
    ]
