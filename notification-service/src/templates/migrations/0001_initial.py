# Generated by Django 4.0.6 on 2022-07-29 10:41

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Template',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='id')),
                ('subject', models.CharField(max_length=255, verbose_name='title')),
                ('body', models.TextField(verbose_name='template_body')),
            ],
        ),
    ]
