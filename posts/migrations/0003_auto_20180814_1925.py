# Generated by Django 2.1 on 2018-08-14 19:25

from django.db import migrations, models
import django.db.models.deletion
import posts.models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0002_auto_20180813_1240'),
    ]

    operations = [
        migrations.CreateModel(
            name='MediaFile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(max_length=255, upload_to=posts.models.generate_filename)),
                ('filename', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='media_files', to='posts.Post')),
            ],
        ),
        migrations.AlterModelOptions(
            name='like',
            options={'ordering': ['-created_at'], 'verbose_name': 'Like', 'verbose_name_plural': 'Likes'},
        ),
    ]