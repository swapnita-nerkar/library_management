# Generated by Django 3.1.1 on 2020-09-15 09:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0016_auto_20200915_1451'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='student',
            name='branch',
        ),
        migrations.AddField(
            model_name='student',
            name='department',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='management.department'),
        ),
        migrations.AlterField(
            model_name='book',
            name='Department',
            field=models.ManyToManyField(help_text='Select a Department for this book', to='management.Department'),
        ),
    ]
