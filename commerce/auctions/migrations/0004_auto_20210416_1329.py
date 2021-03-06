# Generated by Django 3.1.7 on 2021-04-16 13:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0003_auto_20210415_0609'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='is_watchlist',
            field=models.CharField(choices=[('YES', 'Yes'), ('NO', 'No')], default='NO', max_length=3),
        ),
        migrations.AlterField(
            model_name='listing',
            name='photo',
            field=models.ImageField(blank=True, null=True, upload_to='images/'),
        ),
        migrations.AlterField(
            model_name='listing',
            name='starting_bid',
            field=models.DecimalField(decimal_places=1, default=1.0, max_digits=7),
        ),
    ]
