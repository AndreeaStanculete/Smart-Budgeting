# Generated by Django 4.2.4 on 2024-05-27 10:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('budgetingApp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='OneTimeLink',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('UniqueCode', models.CharField(max_length=20)),
                ('AssociatedEMail', models.CharField(max_length=50)),
            ],
        ),
    ]
