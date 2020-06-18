# Generated by Django 3.0.7 on 2020-06-18 22:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Collection',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('owning_auth_user_id', models.IntegerField()),
                ('collection_name', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Collection_Content',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('obtained', models.BooleanField()),
                ('card_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.Card')),
                ('collection_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.Collection')),
            ],
        ),
    ]