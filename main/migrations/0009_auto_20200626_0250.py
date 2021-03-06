# Generated by Django 3.0.7 on 2020-06-26 02:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0008_auto_20200625_0829'),
    ]

    operations = [
        migrations.RenameField(
            model_name='card',
            old_name='cmc',
            new_name='converted_mana_cost',
        ),
        migrations.RenameField(
            model_name='card',
            old_name='tcg_id',
            new_name='mtg_json_uuid',
        ),
        migrations.RemoveField(
            model_name='card',
            name='prices',
        ),
        migrations.AddField(
            model_name='card',
            name='tcgplayer_id',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='listing',
            name='card_market_purchase_url',
            field=models.CharField(default='https://www.cardmarket.com/en', max_length=2000),
        ),
        migrations.AddField(
            model_name='listing',
            name='mtg_stocks_purchase_url',
            field=models.CharField(default='https://www.mtgstocks.com/news', max_length=2000),
        ),
        migrations.AddField(
            model_name='listing',
            name='tcg_player_purchase_url',
            field=models.CharField(default='https://www.tcgplayer.com/', max_length=2000),
        ),
    ]
