# Generated by Django 5.0.6 on 2025-03-22 08:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0020_alter_bookingslot_slot_time'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bookingslot',
            name='available_tables',
        ),
        migrations.RemoveField(
            model_name='bookingslot',
            name='slot_time',
        ),
        migrations.AddField(
            model_name='bookingslot',
            name='time',
            field=models.TimeField(default='11:00:00'),
        ),
    ]
