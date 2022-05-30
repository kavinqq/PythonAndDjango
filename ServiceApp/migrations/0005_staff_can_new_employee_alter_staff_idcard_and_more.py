# Generated by Django 4.0.4 on 2022-05-27 01:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ServiceApp', '0004_remove_staff_staffid'),
    ]

    operations = [
        migrations.AddField(
            model_name='staff',
            name='can_new_employee',
            field=models.BooleanField(default=False, help_text='是否能 新增員工', verbose_name='權限：新增員工'),
        ),
        migrations.AlterField(
            model_name='staff',
            name='IdCard',
            field=models.CharField(help_text='身分證', max_length=100, verbose_name='身分證'),
        ),
        migrations.AlterField(
            model_name='staff',
            name='authority',
            field=models.IntegerField(default=10, help_text='數字越小 權限越大 superuser = -1', verbose_name='權限'),
        ),
        migrations.AlterField(
            model_name='staff',
            name='can_check_status',
            field=models.BooleanField(default=False, help_text='是否能 查看會員狀態', verbose_name='權限：查看狀態'),
        ),
        migrations.AlterField(
            model_name='staff',
            name='can_reset_password',
            field=models.BooleanField(default=False, help_text='是否能 重置密碼', verbose_name='權限：重置密碼'),
        ),
        migrations.AlterField(
            model_name='staff',
            name='can_search_username',
            field=models.BooleanField(default=False, help_text='是否能 查詢帳號', verbose_name='權限：查詢帳號'),
        ),
        migrations.AlterField(
            model_name='staff',
            name='can_unlock',
            field=models.BooleanField(default=False, help_text='是否能 解鎖帳號', verbose_name='權限：解鎖帳號'),
        ),
        migrations.AlterField(
            model_name='staff',
            name='phoneNumber',
            field=models.CharField(help_text='手機號碼', max_length=100, verbose_name='手機號碼'),
        ),
    ]