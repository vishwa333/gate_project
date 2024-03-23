# Generated by Django 3.2.25 on 2024-03-23 12:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('questions', '0001_initial'),
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='test',
            fields=[
                ('test_id', models.AutoField(primary_key=True, serialize=False, unique=True)),
                ('test_type', models.CharField(choices=[('Chapter_wise', 'Chapter_wise'), ('Subject_wise', 'Subject_wise'), ('Part_syllabus', 'Part_syllabus'), ('Multi_sub', 'Multi_sub'), ('Full_length', 'Full_length')], default='Test', max_length=40)),
                ('max_marks', models.IntegerField()),
                ('max_time', models.IntegerField(default=10)),
                ('difficulty', models.CharField(choices=[('Mixed', 'Mixed'), ('Easy', 'Easy'), ('Medium', 'Medium'), ('Hard', 'Hard'), ('Very_hard', 'Very_hard')], default='Easy', max_length=40)),
                ('questions', models.ManyToManyField(to='questions.question')),
                ('tchap', models.ManyToManyField(blank=True, to='questions.chapter')),
                ('tsub', models.ManyToManyField(to='questions.subject')),
            ],
        ),
        migrations.CreateModel(
            name='testtype',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ttype', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='test_result',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('marks', models.FloatField()),
                ('test_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='my_test.test')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.my_user')),
            ],
        ),
        migrations.CreateModel(
            name='test_responses',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('response', models.CharField(max_length=4)),
                ('correctness', models.BooleanField()),
                ('mark', models.FloatField(default=0.0)),
                ('question_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='questions.question')),
                ('test_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='my_test.test')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.my_user')),
            ],
            options={
                'unique_together': {('test_id', 'question_id', 'user_id')},
            },
        ),
    ]
