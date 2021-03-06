# Generated by Django 2.2.9 on 2020-01-23 08:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Sentence',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sentence_id', models.PositiveIntegerField()),
                ('text', models.TextField(max_length=250)),
                ('word', models.CharField(max_length=30)),
                ('word_id', models.PositiveSmallIntegerField(blank=True, null=True)),
                ('Text_index', models.PositiveSmallIntegerField()),
                ('atr', models.PositiveSmallIntegerField(blank=True, null=True)),
                ('trans_word', models.CharField(blank=True, max_length=30, null=True)),
            ],
        ),
        migrations.DeleteModel(
            name='Post',
        ),
    ]
