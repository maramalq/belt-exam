# Generated by Django 2.2.4 on 2021-04-29 15:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=45)),
                ('last_name', models.CharField(max_length=45)),
                ('email', models.CharField(max_length=255)),
                ('password', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Wish',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=45)),
                ('desc', models.CharField(max_length=255)),
                ('granted', models.BooleanField(default=False)),
                ('liked', models.BooleanField(default=False)),
                ('liked_count', models.IntegerField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('granted_by', models.ManyToManyField(related_name='wishes_granted', to='exam_app.User')),
                ('liked_by', models.ManyToManyField(related_name='liked_wishes', to='exam_app.User')),
                ('made_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='wishes_maded', to='exam_app.User')),
            ],
        ),
    ]
