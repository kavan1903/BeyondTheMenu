# Generated by Django 5.0.6 on 2025-03-22 06:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0018_tablebooking_status_alter_tablebooking_booking_time'),
    ]

    operations = [
        migrations.CreateModel(
            name='BookingSlot',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slot_time', models.TimeField(unique=True)),
                ('available_tables', models.IntegerField(default=20)),
            ],
        ),
        migrations.AddField(
            model_name='tablebooking',
            name='email',
            field=models.EmailField(max_length=254, null=True),
        ),
    ]
