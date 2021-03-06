# Generated by Django 3.0.6 on 2021-03-09 09:31

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='fileDoc',
            fields=[
                ('id', models.AutoField(primary_key=True)),
                ('file_id', models.CharField(max_length=256)),
                ('name', models.CharField(max_length=256, null=True)),
                ('size', models.IntegerField()),
                ('url', models.URLField(max_length=500)),
            ],
        ),
    ]
