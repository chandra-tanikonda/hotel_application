# Generated by Django 5.1.2 on 2024-11-10 22:35

import django.contrib.auth.models
import django.contrib.auth.validators
import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('room_num', models.CharField(max_length=5, unique=True)),
                ('room_type', models.CharField(choices=[('SQN', 'Single Queen'), ('SKN', 'Single King'), ('DQN', 'Double Queen'), ('DKN', 'Double King'), ('SKS', 'Suite King')], max_length=3)),
                ('room_capacity', models.IntegerField(null=True)),
                ('price_per_night', models.DecimalField(decimal_places=2, max_digits=6)),
                ('is_available', models.BooleanField(default=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='room_images/')),
                ('details', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Services',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('rate_per_night', models.DecimalField(decimal_places=2, max_digits=6)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('service_details', models.CharField(max_length=100, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('first_name', models.CharField(max_length=60, null=True)),
                ('last_name', models.CharField(max_length=30, null=True)),
                ('email', models.CharField(max_length=100, null=True)),
                ('mobile_number', models.CharField(max_length=12, null=True)),
                ('address', models.TextField(blank=True)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='PaymentDetail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name_on_card', models.CharField(max_length=120)),
                ('card_type', models.CharField(max_length=60)),
                ('card_number', models.CharField(max_length=18)),
                ('exp_month', models.PositiveSmallIntegerField()),
                ('exp_year', models.PositiveSmallIntegerField()),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Reservation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_in', models.DateField()),
                ('date_out', models.DateField()),
                ('total_cost', models.DecimalField(decimal_places=2, max_digits=8)),
                ('is_active', models.BooleanField(default=True)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('room', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='hotel_app.room')),
            ],
        ),
        migrations.CreateModel(
            name='PaymentTransaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('transaction_amount', models.DecimalField(decimal_places=2, max_digits=9)),
                ('transaction_date', models.DateTimeField(auto_now_add=True)),
                ('transaction_method', models.CharField(max_length=50)),
                ('transaction_status', models.CharField(max_length=50)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('payment_detail', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='hotel_app.paymentdetail')),
                ('reservation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hotel_app.reservation')),
            ],
        ),
        migrations.CreateModel(
            name='ReservationService',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('count', models.PositiveIntegerField(default=1)),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now)),
                ('last_updated', models.DateTimeField(auto_now=True)),
                ('reservation', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='reservation_services', to='hotel_app.reservation')),
                ('extra_service', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='hotel_app.services')),
            ],
        ),
    ]
