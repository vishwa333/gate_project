# Generated by Django 3.2.25 on 2024-03-29 16:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='topic',
            field=models.ForeignKey(default='unassigned', on_delete=django.db.models.deletion.SET_DEFAULT, to='questions.topic'),
        ),
        migrations.AlterField(
            model_name='topic',
            name='topic_code',
            field=models.CharField(max_length=6, primary_key=True, serialize=False),
        ),
    ]
