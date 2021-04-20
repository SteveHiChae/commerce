# Generated by Django 3.1.7 on 2021-04-18 02:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0006_auto_20210417_2338'),
    ]

    operations = [
        migrations.RenameField(
            model_name='listing',
            old_name='name',
            new_name='title',
        ),
        migrations.AddField(
            model_name='listing',
            name='description',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='listing',
            name='category',
            field=models.CharField(blank=True, choices=[('COLTBLE', 'Collectible & art'), ('ELECTRO', 'Electronics'), ('FASHION', 'Fashion'), ('HOME', 'Home & garden'), ('MUSIC', 'Musical Instruments & garden'), ('TOY', 'Toys & hobbies')], default='TOY', max_length=10, null=True),
        ),
    ]