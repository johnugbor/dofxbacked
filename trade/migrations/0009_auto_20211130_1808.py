# Generated by Django 3.1.4 on 2021-11-30 17:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trade', '0008_auto_20211130_1744'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tradetransaction',
            name='user',
            field=models.CharField(max_length=555, null=True),
        ),
    ]