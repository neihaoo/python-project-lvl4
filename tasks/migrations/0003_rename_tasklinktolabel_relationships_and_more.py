# Generated by Django 4.0.6 on 2022-07-15 08:33

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('labels', '0001_initial'),
        ('tasks', '0002_tasklinktolabel_task_labels_tasklinktolabel_task'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='TaskLinkToLabel',
            new_name='Relationships',
        ),
        migrations.AlterField(
            model_name='task',
            name='created_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='created_by', to=settings.AUTH_USER_MODEL),
        ),
    ]