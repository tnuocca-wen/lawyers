# Generated by Django 5.1.3 on 2024-11-25 13:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('skapp', '0002_rename_article_id_sk_sk_id_sk_datetime'),
    ]

    operations = [
        migrations.RenameField(
            model_name='sk',
            old_name='keytakeaways',
            new_name='notes',
        ),
        migrations.RenameField(
            model_name='sk',
            old_name='summary',
            new_name='timeline',
        ),
        migrations.AddField(
            model_name='sk',
            name='description',
            field=models.CharField(default='', max_length=1000),
            preserve_default=False,
        ),
    ]
