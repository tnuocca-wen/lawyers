# Generated by Django 5.1.3 on 2024-11-23 07:25

import skapp.models
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Sk',
            fields=[
                ('article_id', models.IntegerField(primary_key=True, serialize=False, validators=[skapp.models.validate_gt])),
                ('summary', models.TextField()),
                ('keytakeaways', models.TextField()),
                ('filename', models.CharField(max_length=100)),
                ('inputfile', models.FileField(null=True, upload_to='input_files/')),
            ],
        ),
    ]
