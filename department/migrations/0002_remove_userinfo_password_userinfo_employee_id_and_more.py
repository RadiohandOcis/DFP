# Generated by Django 4.0.5 on 2022-06-18 09:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('department', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userinfo',
            name='password',
        ),
        migrations.AddField(
            model_name='userinfo',
            name='employee_id',
            field=models.CharField(default=123, max_length=64, verbose_name='工号'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='userinfo',
            name='salary',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='薪资'),
        ),
    ]
