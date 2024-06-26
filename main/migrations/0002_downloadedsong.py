# Generated by Django 4.2.4 on 2024-05-02 04:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='DownloadedSong',
            fields=[
                ('id_song', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='main.song')),
                ('email_downloader', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.premium')),
            ],
            options={
                'unique_together': {('id_song', 'email_downloader')},
            },
        ),
    ]
