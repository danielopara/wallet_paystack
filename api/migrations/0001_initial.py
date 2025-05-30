# Generated by Django 5.1.7 on 2025-03-30 17:39

import django.db.models.deletion
import django.utils.timezone
import uuid
from decimal import Decimal
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Wallet',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('balance', models.DecimalField(decimal_places=2, default=Decimal('0.00'), max_digits=15)),
                ('currency', models.CharField(default='NGN', max_length=50)),
                ('user', models.OneToOneField(db_column='user_username', on_delete=django.db.models.deletion.CASCADE, related_name='user_wallet', to=settings.AUTH_USER_MODEL, to_field='username')),
            ],
        ),
        migrations.CreateModel(
            name='Wallet_Transaction',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=15)),
                ('transaction_type', models.CharField(choices=[('deposit', 'deposit'), ('transfer', 'transfer'), ('withdraw', 'withdraw')], max_length=10)),
                ('reference', models.CharField(max_length=100, unique=True)),
                ('status', models.CharField(default='pending', max_length=20)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('wallet', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='transactions', to='api.wallet')),
            ],
        ),
    ]
