# Generated by Django 3.1.4 on 2021-11-15 19:02

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Wallet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('balance', models.FloatField()),
                ('user_id', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.FloatField()),
                ('transaction_type', models.CharField(choices=[('BUY', 'Buy'), ('SELL', 'Sell'), ('DEPO', 'Deposit'), ('WITHD', 'Withdrawal')], default='WITHD', max_length=5)),
                ('wallet_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='trade.wallet')),
            ],
        ),
    ]
