# Generated by Django 3.2 on 2020-07-16 21:03

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('main', '0017_alter_bazaar_user_location'),
    ]

    operations = [
        migrations.CreateModel(
            name='User_Preferences',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('allow_email', models.BooleanField()),
                ('subscribe_email', models.BooleanField()),
                ('view_email', models.BooleanField()),
                ('user_id', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]