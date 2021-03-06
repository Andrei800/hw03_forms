# Generated by Django 2.2.19 on 2021-11-15 22:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0004_auto_20211115_2218'),
    ]

    operations = [
        migrations.RenameField(
            model_name='group',
            old_name='slag',
            new_name='slug',
        ),
        migrations.AlterField(
            model_name='post',
            name='group',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='group', to='posts.Group', verbose_name='Группа'),
        ),
    ]
